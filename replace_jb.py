import json
import subprocess
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    MofNCompleteColumn,
    TextColumn,
    TimeRemainingColumn,
    TimeElapsedColumn
)
from rich.console import Console
import win32api
import win32file
import os
import sys
from shutil import copy2, rmtree
from pathlib import Path
from PIL import Image
from copy import copy


idea_names = [
    "PyCharm",
    "RustRover",
    "CLion"
]
console = Console(color_system='truecolor')
print = console.print


def get_drives():
    drives = [i for i in win32api.GetLogicalDriveStrings().split('\x00') if i]
    rdrives = [d for d in drives if win32file.GetDriveType(d) == win32file.DRIVE_FIXED]
    return rdrives


def traverse_dirs(path, max_deepth: int = 255, deepth: int = 0, progress_task: int = None):
    files = []
    if deepth > max_deepth:
        return []
    try:
        handle = win32file.FindFilesW(path + '\\*')
        for h in handle:
            filename = h[8]
            if filename not in ['.', '..', 'Windows', 'EFI', 'Temp']:
                fullname = path + '\\' + filename
                if progress_task and deepth == 0:
                    p.update(progress_task, description=fullname.replace('\\\\', '\\'))
                if win32file.GetFileAttributes(fullname) == win32file.FILE_ATTRIBUTE_DIRECTORY:
                    files.append(fullname.replace('\\\\', '\\'))
                    files.extend(traverse_dirs(fullname, max_deepth=max_deepth, deepth=deepth+1))
                    if progress_task and deepth == 0:
                        p.advance(progress_task)
    except:
        pass
    finally:
        return files


def resize_image(img: Image, new_dimensions, output_path):
    img: Image = copy(img)
    new_img = Image.new('RGBA', new_dimensions)
    ratio = min(new_dimensions[0] / img.width, new_dimensions[1] / img.height)
    resized_dimensions = (int(img.width * ratio), int(img.height * ratio))
    resized_img = img.resize(resized_dimensions, Image.Resampling.LANCZOS)
    x = (new_dimensions[0] - resized_dimensions[0]) // 2
    y = (new_dimensions[1] - resized_dimensions[1]) // 2
    new_img.paste(resized_img, (x, y))
    new_img.save(output_path, "PNG")



drives = get_drives()
if len(sys.argv) == 1:
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TextColumn("/"),
        TimeRemainingColumn()) as p:
        sct = p.add_task(description="Scan", total=len(drives))
        idea_dirs = []
        for d in drives:
            root_dirs = traverse_dirs(d, 0)
            dt = p.add_task(description=d, total=len(root_dirs))
            dirs = traverse_dirs(d, 2, progress_task=dt)
            dirs = [(x, x.split("\\")[-1]) for x in dirs]
            dirs = [x[0] for x in dirs if list(filter(lambda y: y in x[1], idea_names))]
            idea_dirs += dirs
            p.advance(sct)
    if idea_dirs:
        for i in range(len(idea_dirs)):
            print(f"{i+1}. {idea_dirs[i]}")
        i = int(input("Select Current Dir No. (or 0 to specific path): "))
        if i:
            curr_dir = Path(idea_dirs[i-1])
        else:
            curr_dir = Path(input("IDE path(root path, not 'bin' dir): "))
            if not curr_dir.exists():
                raise FileNotFoundError(f"{curr_dir} is not exists.")
    else:
        print("Cannot found JetBrains IDE, please specific the install path")
        curr_dir = Path(input("IDE path(root path, not 'bin' dir): "))
        if not curr_dir.exists():
            raise FileNotFoundError(f"{curr_dir} is not exists.")
else:
    curr_dir = Path(sys.argv[1])
    if not curr_dir.exists():
        raise FileNotFoundError(f"{curr_dir} is not exists.")

print(f"Selected dir '{curr_dir}'")

version = (curr_dir.name, 0)
if Path(curr_dir, "product-info.json").exists():
    with open(Path(curr_dir, "product-info.json"), 'r') as f:
        pdi = json.loads(f.read())
    version = (pdi['name'], pdi['version'])
print(f"IDE: [green]{version[0]}[/] [yellow]{version[1]}[/]")
if int(version[1].split(".")[0]) >= 2024:
    if not Path(curr_dir, 'lib', 'app.jar').exists():
        print(f"Path {Path(curr_dir, 'lib', 'app.jar')} is not exists!")
        sys.exit(1)
elif int(version[1].split(".")[0]) >= 2023:
    raise NotImplementedError("Searing methods.")
else:
    raise RuntimeError(f"Unsupport IDE version: {version[1]}")
img_path = Path(input("Replace image locate(Absolute Path): "))
if not img_path.exists():
    raise FileNotFoundError(f"'{img_path}' does not exists.")
replace_img = Image.open(str(img_path))
if not Path(curr_dir, 'lib').exists():
    raise FileNotFoundError(f"'{Path(curr_dir, 'lib')}' does not exists.Maybe you should install IDE again?")
os.chdir(Path(curr_dir, 'lib'))
try:
    process = subprocess.run("jar --version")
    if process.returncode:
        raise RuntimeError(process.stdout)
except Exception as err:
    print(f"[red bold]{err.__class__.__name__}[/]: [bold white]{err}[/]")
    print("[yellow]Note[/]: Maybe you have [red]not install[/] java?")
    sys.exit(1)
if not Path(curr_dir, 'lib', 'app.jar.bak').exists():
    copy2(Path(curr_dir, 'lib', 'app.jar'), Path(curr_dir, 'lib', 'app.jar.bak'))
if Path(curr_dir, 'lib', '.ReplaceLogo').exists():
    rmtree(Path(curr_dir, 'lib', '.ReplaceLogo'))
os.mkdir(".ReplaceLogo")
os.chdir(Path(curr_dir, 'lib', ".ReplaceLogo"))
copy2(Path(curr_dir, 'lib', 'app.jar'), Path(curr_dir, 'lib', '.ReplaceLogo'))
with Progress(
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    ) as p:
    jt = p.add_task(description=' '.join(['jar', '-xvf', str(Path(curr_dir, 'lib', '.ReplaceLogo', 'app.jar'))]), total=1)
    process = subprocess.Popen(['jar', '-xvf', str(Path(curr_dir, 'lib', '.ReplaceLogo', 'app.jar'))], stdout=subprocess.PIPE, text=True)
    for line in process.stdout:
        pass
    p.advance(jt)
    if process.returncode:
        raise RuntimeError(f"Process exited with code {process.returncode}")
    os.remove(Path(curr_dir, 'lib', '.ReplaceLogo', 'app.jar'))
    if int(version[1].split(".")[0]) >= 2024:
        for f in ["pycharm_logo@2x.png", "pycharm_logo.png"]:
            raw_img = Path(curr_dir, 'lib', '.ReplaceLogo', f)
            if not raw_img.exists():
                raise FileNotFoundError(f"'{raw_img}' does not exists.")
            os.remove(raw_img)
            if '2x' in f:
                resize_image(replace_img, (1280, 800), raw_img)
            else:
                resize_image(replace_img, (640, 400), raw_img)
    elif int(version[1].split(".")[0]) >= 2023:
        raise NotImplementedError("Searing methods.")
    else:
        raise RuntimeError("Unsupport IDE version.")
    jt = p.add_task(description=' '.join(['jar', '-cfM0', str(Path(curr_dir, 'lib', '.ReplaceLogo', 'app.jar'))]), total=1)
    process = subprocess.Popen(['jar', '-cfM0', '../app.jar', './'], stdout=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line, end='')
    p.advance(jt)
if Path(curr_dir, "product-info.json").exists():
    try:
        with open(Path(curr_dir, "product-info.json"), 'r') as f:
            pdi = json.loads(f.read())
        version = pdi['name'] + pdi['version']
        cache_dir = Path(os.getenv("USERPROFILE"), f"AppData/Local/JetBrains/{version}/splash")
        rmtree(cache_dir)
        os.mkdir(cache_dir)
        print("Auto deleted cache.")
        sys.exit(0)
    except Exception as err:
        print(err.__class__.__name__, err)
print(f'Remove files under ~/AppData/Local/JetBrains/[IDE Name]/splash to apply the change.')
    

