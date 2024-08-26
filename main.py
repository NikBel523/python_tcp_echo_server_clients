import asyncio
import logging

from data_base import init_db
from client import tcp_client
from server import start_server


CLIENT_TASKS_NUM = 10


# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


async def main():
    """Основная логика."""
    # Инициализация базы данных
    conn = init_db()

    server_task = asyncio.create_task(start_server(conn))

    # Запуск 10 клиентов
    client_tasks = [asyncio.create_task(tcp_client(i)) for i in range(1, CLIENT_TASKS_NUM + 1)]

    # Ожидание завершения всех клиентских задач
    await asyncio.gather(*client_tasks)

    # Остановка сервера после завершения всех клиентов
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        logging.info("Server остановлен")
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Программа завершена вручную")
