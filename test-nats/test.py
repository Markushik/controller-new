import asyncio
import nats


async def main():
    nc = await nats.connect('127.0.0.1:4222')
    js = nc.jetstream()

    await js.publish("test_stream.test", b'last?')
    psub = await js.pull_subscribe("test_stream.test", "durable")
    msgs = await psub.fetch(1)
    msg = msgs[0]
    await msg.nak(1000)

    # while True:
    #     try:
    #         ...
    #         # msg = await sub.next_msg()
    #     except TimeoutError:
    #         break
    #     # print('----------------------')
    #     # print('Subject:', msg.subject)
    #     # print('Reply  :', msg.reply)
    #     # print('Data   :', msg.data)
    #     # print('Headers:', msg.header)


if __name__ == '__main__':
    asyncio.run(main())
