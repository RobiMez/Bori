# ''' Cat pictures and gifs '''
# import sys
# import requests , re
# import asyncio 
# import traceback
# from telethon import events
# from pathlib import Path
# from ubi import u 
# import importlib

# def admin_cmd(pattern):
#     return events.NewMessage(outgoing=True, pattern=re.compile(pattern))


# DELETE_TIMEOUT = 2


# @u.on(admin_cmd(r"^\.load (?P<shortname>\w+)$"))
# async def load_reload(event):
#     await event.delete()
#     shortname = event.pattern_match["shortname"]



# @u.on(admin_cmd(r"^\.(?:unload) (?P<shortname>\w+)$"))
# async def remove(event):
#     await event.delete()
#     shortname = event.pattern_match["shortname"]




# def load_module(shortname, plugin_path=None):
#     if shortname.startswith("__"):
#         pass
#     elif shortname.endswith("_"):
#         path = Path(f"userbot/plugins/{shortname}.py")
#         name = "userbot.plugins.{}".format(shortname)
#         spec = importlib.util.spec_from_file_location(name, path)
#         mod = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(mod)
#         print(f"Successfully imported {shortname}")
#     else:
#         if plugin_path is None:
#             path = Path(f"userbot/plugins/{shortname}.py")
#             name = f"userbot.plugins.{shortname}"
#         else:
#             path = Path((f"{plugin_path}/{shortname}.py"))
#             name = f"{plugin_path}/{shortname}".replace("/", ".")
#         spec = importlib.util.spec_from_file_location(name, path)
#         mod = importlib.util.module_from_spec(spec)
#         mod.bot = u
#         spec.loader.exec_module(mod)
#         # for imports
#         sys.modules[f"userbot.plugins.{shortname}"] = mod
#         print(f"Successfully imported {shortname}")


# def remove_plugin(shortname):
#     try:
#         cmd = []
#         if shortname in PLG_INFO:
#             cmd += PLG_INFO[shortname]
#         else:
#             cmd = [shortname]
#         for cmdname in cmd:
#             if cmdname in LOADED_CMDS:
#                 for i in LOADED_CMDS[cmdname]:
#                     catub.remove_event_handler(i)
#                 del LOADED_CMDS[cmdname]
#         return True
#     except Exception as e:
#         LOGS.error(e)
#     try:
#         for i in LOAD_PLUG[shortname]:
#             catub.remove_event_handler(i)
#         del LOAD_PLUG[shortname]
#     except BaseException:
#         pass
#     try:
#         name = f"userbot.plugins.{shortname}"
#         for i in reversed(range(len(catub._event_builders))):
#             ev, cb = catub._event_builders[i]
#             if cb.__module__ == name:
#                 del catub._event_builders[i]
#     except BaseException as exc:
#         raise ValueError from exc
