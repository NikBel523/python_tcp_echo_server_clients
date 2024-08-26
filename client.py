import asyncio
import random
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


async def tcp_client(client_id):
    """Сопрограмма TCP-клиента."""
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    for i in range(5):
        message = f'Сообщение {i+1} от клиента {client_id}'
        logging.info(f"Клиент {client_id} отправляет: {message}")
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(100)
        logging.info(f"Клиент {client_id} получил: {data.decode()}")

        await asyncio.sleep(random.uniform(5, 10))

    logging.info(f"Клиент {client_id} закрывает соединение")
    writer.close()
    await writer.wait_closed()
