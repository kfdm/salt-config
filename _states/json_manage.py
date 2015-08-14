import json
import os

__virtualname__ = 'json'

def __virtual__():
    return __virtualname__

def manage(name, context, indent=4):
    ret = {'name': name, 'changes': {}, 'result': False, 'comment': ''}

    with open(name, 'r+') as fp:
        config = json.load(fp)
        for key, value in context.items():
           if key in config and config[key] != value:
               ret['changes'][key] = {'old': config[key], 'new': value}
               if not __opts__['test']:
                   config[key] = value
           if key not in config:
               ret['changes'][key] = {'old': None, 'new': value}
               if not __opts__['test']:
                   config[key] = value
        if __opts__['test']:
            ret['result'] = None
        else:
            fp.seek(0)
            json.dump(config, fp, indent=indent)
            ret['comment'] = 'Wrote values to ' + name
            ret['result'] = True

    return ret


