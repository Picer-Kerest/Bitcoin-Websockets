import websockets
import asyncio
import json
import time
import matplotlib.pyplot as plt

xdata = []
ydata = []


fig = plt.figure()
ax = fig.add_subplot(111)
fig.show()


def update_graph():
    ax.plot(xdata, ydata)
    # рисуем график
    fig.canvas.draw()
    plt.pause(0.1)


async def main():
    url = "wss://stream.binance.com:9443/stream?streams=btcusdt@miniTicker"
    async with websockets.connect(url) as client:
        # websockets.connect(url) устанавливаем соединение по указанному адресу
        while True:
            data = json.loads(await client.recv())['data']
            # await client.recv() тип строка. Конвертируем в словарь и берём data
            event_time = time.localtime(data['E'] // 1000)
            event_time = f"{event_time.tm_hour}:{event_time.tm_min}:{event_time.tm_sec}"
            print(event_time, '->', data['c'])
            xdata.append(event_time)
            ydata.append(int(float(data['c'])))
            update_graph()


if __name__ == '__main__':
    asyncio.run(main())

