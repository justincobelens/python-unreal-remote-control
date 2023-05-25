import asyncio

from pyunreal.utils import pretty_print
from pyunreal.client import Client


async def main():
    client = Client()
    # info = await client.info()
    # pretty_print(info)
    # print(await client.presets())
    preset = await client.preset("TestRC")
    # pretty_print(preset._preset_info)
    # groups = await preset.get_all_groups()
    # # print(len(groups))
    #
    # group_1 = await preset.get_group("All")
    # pretty_print(group_1)
    # properties = await preset.get_all_properties_names()
    # print(properties)
    prop = await preset.get_property('Relative Location (TestSphere)')
    # print(prop)
    print('\n\n')
    pretty_print(await prop.value())
    await prop.set(Z=0)
    await prop.set(Z=200)
    await prop.set(Z=0)
    # pretty_print(await prop.value())
    # actors = await preset.get_all_actors()
    # print('\n\n ***************************** \n\n')
    # # pretty_print(actors)

    await client.close_connection()

if __name__ == '__main__':
    asyncio.run(main())
