from pathlib import Path
import re

root = Path('.')
dist = root / 'dist'
assets = root / 'assets' / 'editorial-v2'
dist.mkdir(exist_ok=True)

def nested(path, x, y, width, height):
    svg = path.read_text(encoding='utf-8')
    # Explicit dimensions position each self-contained SVG without browser layout gaps.
    svg = re.sub(r'<svg\b', f'<svg x="{x}" y="{y}"', svg, count=1)
    svg = re.sub(r'\bwidth="[^"]+"', f'width="{width}"', svg, count=1)
    svg = re.sub(r'\bheight="[^"]+"', f'height="{height}"', svg, count=1)
    # A single profile graphic cannot expose individual click targets. Show the
    # email address as information rather than implying a clickable button.
    svg = svg.replace('Email me  →', 'khalil.moftah@gmail.com').replace('Email me →', 'khalil.moftah@gmail.com')
    return svg

for theme in ('light', 'dark'):
    bg = '#14202b' if theme == 'dark' else '#f7f3e9'
    snake_file = dist / ('github-contribution-grid-snake-dark.svg' if theme == 'dark' else 'github-contribution-grid-snake.svg')
    for mobile in (False, True):
        variant = '-mobile' if mobile else ''
        width = 450 if mobile else 900
        names = ['intro', 'row1', 'row2', 'footer']
        heights = [720, 1040, 1040, 380] if mobile else [685, 438, 438, 269]
        bottom = sum(heights)
        snake_width = width - (40 if mobile else 64)
        snake_height = round(snake_width * 192 / 880)
        gap = 16 if mobile else 24
        height = bottom + gap + snake_height + gap
        pieces = []
        y = 0
        for name, section_height in zip(names, heights):
            pieces.append(nested(assets / f'{name}{variant}-{theme}.svg', 0, y, width, section_height))
            y += section_height
        pieces.append(nested(snake_file, (width-snake_width)//2, bottom+gap, snake_width, snake_height))
        document = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                    f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
                    f'<rect width="{width}" height="{height}" fill="{bg}"/>' + ''.join(pieces) + '</svg>')
        (dist / f'profile{variant}-{theme}.svg').write_text(document, encoding='utf-8')
        print(f'Built profile{variant}-{theme}.svg ({len(document)} characters)')
