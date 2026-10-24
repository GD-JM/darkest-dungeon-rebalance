"""WS-MODULAR-001: one-time, explicitly approved six-package registration.

Creation is never retried after an ambiguous outcome. IDs are durable before
any subsequent mutation. New items stay private until the main-push publisher.
"""
import argparse
from pathlib import Path
from common import read_json, write_json, WorkerLock
from steam import Steam, SteamError

KEYS = ('base', 'duelist', 'runaway', 'flagellant', 'shieldbreaker', 'musketeer')
DLC = {'duelist':4964110, 'runaway':4964110, 'flagellant':580100,
       'shieldbreaker':702540, 'musketeer':445700}


def register(config, output):
    root = Path(config['state_dir'])
    path = root / 'modules-create.json'
    state = read_json(path, {})
    with WorkerLock(root / 'worker.lock'):
        for key in KEYS:
            record = state.setdefault(key, {'status':'ready'})
            if record['status'] == 'creating':
                raise SteamError('Uncertain prior creation for '+key+'; inspect owned items, never blindly retry')
            if 'item_id' not in record:
                with Steam(config['game_root']) as steam:
                    if not steam.query()['owned']:
                        raise SteamError('Expected Workshop owner is not logged in')
                    def before():
                        record['status'] = 'creating'
                        write_json(path, state)
                    record.update(steam.create_item(before), status='created')
                    write_json(path, state)
            if record.get('needs_agreement'):
                raise SteamError('Steam requires owner acceptance of Workshop agreement; item ID saved')
            if record['status'] == 'created':
                with Steam(config['game_root'], record['item_id']) as steam:
                    steam.update(title='Every Hero Worth Taking - '+key.title()+' (preparing)',
                                 description='Optional package being prepared. Not released yet.', visibility=2)
                record['status'] = 'private'
                write_json(path, state)
            print(key, record['item_id'], record['status'], flush=True)
        registry = {key:{'item_id':state[key]['item_id'], **({'dlc_id':DLC[key]} if key in DLC else {})} for key in KEYS}
        write_json(output, registry)
    return registry


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', default=str(Path(__file__).with_name('config.json')))
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    register(read_json(args.config), Path(args.output))
