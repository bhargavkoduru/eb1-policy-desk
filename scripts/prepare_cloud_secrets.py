"""Create deployment settings locally. Never print credentials or access codes."""
import json
import secrets
from eb1.config import ROOT, api_key
from eb1.access import password_hash


def main():
    target = ROOT / 'runtime/deployment'
    target.mkdir(parents=True, exist_ok=True)
    config_path = target / 'streamlit.secrets.toml'
    access_path = target / 'VIEWER_ACCESS.txt'
    if config_path.exists() or access_path.exists():
        if not (config_path.exists() and access_path.exists()):
            raise ValueError('Incomplete deployment settings: inspect locally before regenerating.')
        print('Existing deployment settings reused; no codes were changed.')
        return
    codes = {name: secrets.token_urlsafe(24) for name in ('owner', 'examiner')}
    lines = ['# Copy into Streamlit Advanced settings > Secrets. Never upload this file to GitHub.',
             'EB1_HOSTED = true', 'EB1_ENABLE_LIVE_CALLS = true',
             'NEBIUS_API_KEY = ' + json.dumps(api_key()),
             'EB1_VIEWER_DAILY_ACTIONS = 30', 'EB1_GLOBAL_DAILY_ACTIONS = 100',
             'EB1_VIEWER_DAILY_ATTEMPTS = 120', 'EB1_GLOBAL_DAILY_ATTEMPTS = 400', '', '[viewers]']
    lines += [name + ' = ' + json.dumps(password_hash(code)) for name, code in codes.items()]
    config_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    access_path.write_text('PRIVATE: do not upload to GitHub or the submission ZIP.\n'
                           'Share only the examiner login through your private course submission.\n'
                           'Anyone using the same username shares that username\'s research workspace.\n\n'
                           + '\n\n'.join('Username: ' + name + '\nAccess code: ' + code for name, code in codes.items()), encoding='utf-8')
    print(json.dumps({'secrets_file': str(config_path), 'access_file': str(access_path), 'credentials_printed': False}))


if __name__ == '__main__':
    main()
