from flask import Flask, render_template_string
import subprocess
import os
import sys

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <meta name="theme-color" content="#0b0d12">
    <meta name="color-scheme" content="dark">
    <title>Пульт управления</title>
    <style>
        :root {
            --bg: #0b0d12;
            --panel: rgba(255, 255, 255, 0.035);
            --line: rgba(255, 255, 255, 0.09);
            --text: #eef1f7;
            --muted: #8b93a7;
        }

        * { box-sizing: border-box; }

        body {
            margin: 0;
            min-height: 100vh;
            min-height: 100dvh;
            display: grid;
            place-items: center;
            padding: 20px 16px calc(20px + env(safe-area-inset-bottom));
            background:
                radial-gradient(1100px 620px at 50% -15%, #1b2233 0%, transparent 62%),
                radial-gradient(820px 520px at 105% 115%, #1a1526 0%, transparent 58%),
                var(--bg);
            color: var(--text);
            font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
            -webkit-font-smoothing: antialiased;
            -webkit-text-size-adjust: 100%;
        }

        .panel {
            width: 100%;
            max-width: 580px;
            padding: 20px;
            border: 1px solid var(--line);
            border-radius: 26px;
            background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.012));
            box-shadow:
                0 40px 90px -50px #000,
                0 1px 0 rgba(255,255,255,0.06) inset;
            backdrop-filter: blur(6px);
        }

        .head {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 4px 4px 18px;
        }

        .pulse {
            width: 9px;
            height: 9px;
            flex: none;
            border-radius: 50%;
            background: #2ee66b;
            box-shadow: 0 0 0 4px rgba(46, 230, 107, 0.14), 0 0 14px #2ee66b;
        }

        .head h1 {
            margin: 0;
            font-size: 1.02rem;
            font-weight: 650;
            letter-spacing: 0.01em;
        }

        .head p {
            margin: 2px 0 0;
            font-size: 0.76rem;
            color: var(--muted);
        }

        .actions {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }

        /* форма не рисует бокс — её кнопка сама становится ячейкой сетки */
        .actions form { display: contents; }

        .btn {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 8px;
            width: 100%;
            min-height: 108px;
            margin: 0;
            padding: 15px 16px;
            border: 1px solid var(--line);
            border-radius: 18px;
            background: linear-gradient(165deg, var(--tint, rgba(255,255,255,0.06)), rgba(255,255,255,0.015));
            color: var(--text);
            font: inherit;
            font-size: 0.94rem;
            font-weight: 650;
            line-height: 1.2;
            text-align: left;
            cursor: pointer;
            -webkit-tap-highlight-color: transparent;
            transition:
                transform 0.16s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease,
                background 0.2s ease;
        }

        .btn .ico { font-size: 1.5rem; line-height: 1; }

        .btn .lbl { display: block; margin-top: auto; }

        .btn .hint {
            font-size: 0.71rem;
            font-weight: 500;
            line-height: 1.35;
            color: var(--muted);
        }

        .btn:active { transform: scale(0.975); }

        .btn:focus-visible {
            outline: 2px solid var(--glow);
            outline-offset: 2px;
        }

        .wide { grid-column: 1 / -1; min-height: 84px; }

        .red    { --tint: rgba(255, 64, 64, 0.16);   --glow: rgba(255, 64, 64, 0.5); }
        .amber  { --tint: rgba(255, 170, 40, 0.14);  --glow: rgba(255, 170, 40, 0.45); }
        .green  { --tint: rgba(46, 230, 107, 0.13);  --glow: rgba(46, 230, 107, 0.42); }
        .violet { --tint: rgba(150, 110, 255, 0.15); --glow: rgba(150, 110, 255, 0.45); }
        .slate  { --tint: rgba(150, 160, 185, 0.10); --glow: rgba(180, 190, 215, 0.35); }

        .foot {
            margin: 16px 4px 2px;
            font-size: 0.7rem;
            line-height: 1.5;
            color: #7c8498;
            text-align: center;
        }

        @media (hover: hover) {
            .btn:hover {
                transform: translateY(-2px);
                border-color: var(--glow);
                box-shadow: 0 16px 34px -18px var(--glow), 0 0 0 1px var(--glow) inset;
            }
        }

        @media (max-width: 400px) {
            body { padding: 12px 12px calc(12px + env(safe-area-inset-bottom)); }
            .panel { padding: 14px; border-radius: 22px; }
            .actions { grid-template-columns: 1fr; }
            .btn { min-height: 92px; }
        }

        @media (prefers-reduced-motion: reduce) {
            .btn { transition: border-color 0.2s ease, box-shadow 0.2s ease; }
            .btn:hover, .btn:active { transform: none; }
        }
    </style>
</head>
<body>
    <main class="panel">
        <header class="head">
            <span class="pulse" aria-hidden="true"></span>
            <div>
                <h1>Пульт управления</h1>
                <p>Выберите действие</p>
            </div>
        </header>

        <div class="actions">
            <form action="/shutdown" method="get">
                <button type="submit" class="btn red">
                    <span class="ico" aria-hidden="true">🔴</span>
                    <span class="lbl">Выключить ПК</span>
                    <span class="hint">Завершение работы</span>
                </button>
            </form>

            <form action="/reboot" method="get">
                <button type="submit" class="btn amber">
                    <span class="ico" aria-hidden="true">🔁</span>
                    <span class="lbl">Перезагрузить ПК</span>
                    <span class="hint">Перезагрузка системы</span>
                </button>
            </form>

            <form action="/glados" method="get">
                <button type="submit" class="btn green">
                    <span class="ico" aria-hidden="true">🖲️</span>
                    <span class="lbl">Запустить Глашу</span>
                    <span class="hint">Голосовой ассистент</span>
                </button>
            </form>

            <form action="/keyboard" method="get">
                <button type="submit" class="btn violet">
                    <span class="ico" aria-hidden="true">⌨️</span>
                    <span class="lbl">Клавиатура</span>
                    <span class="hint">Удалённый ввод</span>
                </button>
            </form>

            <form action="/stop" method="get">
                <button type="submit" class="btn slate wide">
                    <span class="ico" aria-hidden="true">🚨</span>
                    <span class="lbl">Остановить скрипт</span>
                </button>
            </form>
        </div>

        <p class="foot">Доступно из локальной сети</p>
    </main>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/shutdown')
def shutdown():
    subprocess.run('shutdown /s /t 2')
    return 'Система выключается...'

@app.route('/glados')
def glados():
    os.startfile('glados.cmd.lnk')
    return 'Glados...'

@app.route('/stop') 
def stop():
    return 'Останавливаю скрипт'
    sys.exit()

@app.route('/reboot')
def reboot():
    subprocess.run('shutdown /r /t 2')
    return 'Система перезагружается...'

@app.route('/keyboard')
def kb():
    os.startfile('wifi-kb.cmd.lnk')
    return('192.168.3.76:1337')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)