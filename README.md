# ExµArch community machines

Machines that people have built in [ExµArch](https://www.exuarch.com), the computer architecture playground, and shared for others to load, take apart and learn from.

Every machine here shows up in ExµArch on the **Community** tab of the gallery: press **Community** at the top of **Machines** in the getting started drawer. Browse the machines there, and **Add to my machines** copies one into your browser as one of your own, so you can change it as much as you like.

## The placeholder

`machines/placeholder.json` is a placeholder, so the collection does not look empty. It will be removed with the first community contribution: if yours is the first, you can delete it and its entry in `index.json` in your pull request, or leave that to the maintainer.

## Share a machine

1. Build your machine in ExµArch and give it a short note: open **This machine** in the drawer and write what it is and what to try.
2. Press **Export** in the header. You get `<name>.json`, the whole package: the hardware, the microcode, the programs and the note.
3. Fork this repository and put the file in `machines/`, named in lower case without spaces, such as `machines/zed8.json`.
4. Optionally add a picture for the gallery next to it, a PNG of 320 by 240 pixels, such as `machines/zed8.png`.
5. Add an entry for your machine to `index.json`, and open a pull request.

```json
{
  "machines": [
    {
      "name": "ZED-8",
      "author": "Your name",
      "tagline": "An eight bit machine in a day",
      "description": "What it is, what is special about it, and what to try first.",
      "tags": ["8 bit", "lcd"],
      "minVersion": "1.39.0",
      "file": "machines/zed8.json",
      "image": "machines/zed8.png"
    }
  ]
}
```

- `name` must be the same as the `name` in your package file, and unique here. Don't use the name of a machine built into ExµArch, such as `TINY-16`.
- `tagline` is the few words shown next to the name. Keep it under 50 characters.
- `description` is shown when someone opens your machine's details.
- `tags` are topics that search finds it by. Tag it `graphics` if it draws on the screen.
- `minVersion` is the oldest ExµArch your machine works in. Use the version shown at the bottom of the page you built it in. An older ExµArch lists your machine with **Add to my machines** disabled.
- `file` and `image` are paths inside this repository.

A check runs on every pull request. It makes sure `index.json` is valid, that every file is there and is an ExµArch package with the same name, and that nothing is too large: 4 MB for a package and 512 KB for the index.

## Safe to open

An ExµArch package is data, not code: buses, devices, microcode, assembly and Markdown. Opening one can't run anything outside the simulator. The handbook page *Running other people's machines* in ExµArch explains exactly what a package can and can't do.

## License

Every machine shared here is under the MIT license, the same as ExµArch itself. By opening a pull request you agree to share your machine under it.
