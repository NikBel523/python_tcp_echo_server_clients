import asyncio
import logging

from data_base import log_message_to_db


async def handle_client(reader, writer, conn):
    """Обработка соединения клиента с записью данных в базу"""
    addr = writer.get_extra_info("peername")
    logging.info(f"Новое соединение с {addr}")

    while True:
        data = await reader.read(100)
        if not data:
            logging.info(f"Соединение закрыто клиентом {addr}")
            break

        message = data.decode()
        logging.info(f"Получено {message} от {addr}")

        # Преобразование addr в строку перед записью в базу данных
        log_message_to_db(conn, str(addr), message)

        writer.write(data)
        await writer.drain()

    writer.close()
    await writer.wait_closed()


async def start_server(conn):
    """Запуск TCP-сервера с подключением к базе данных"""
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, conn), '127.0.0.1', 8888
    )
    addr = server.sockets[0].getsockname()
    logging.info(f"Server запущен на {addr}")

    async with server:
        await server.serve_forever()
