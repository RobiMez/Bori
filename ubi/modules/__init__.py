from ubi import USERBOT_LOAD, USERBOT_NOLOAD, l


def __list_all_modules():
    from os.path import dirname, basename, isfile
    import glob
    # This generates a list of modules in this folder for the * in __main__ to work.
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [basename(f)[:-3] for f in mod_paths if isfile(f)
                   and f.endswith(".py")
                   and not f.endswith('__init__.py')]

    if USERBOT_LOAD or USERBOT_NOLOAD:
        to_load = USERBOT_LOAD
        if to_load:
            if not all(any(mod == module_name for module_name in all_modules) for mod in to_load):
                l.error("Invalid Module name for userbot!")
                quit(1)
        else:
            to_load = all_modules
        if USERBOT_NOLOAD:
            l.info("Userbot No load: {}".format(USERBOT_NOLOAD))
            return [item for item in to_load if item not in USERBOT_NOLOAD]
        return to_load
    return all_modules


ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]
