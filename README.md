# ![Flow logo](logo@32.png) Flow (modified)

This repository is a **modified version** of [Flow](https://github.com/flow-mn/flow)
(September 2026). It remains free software under the
[GNU General Public License v3](./LICENSE).

Original copyright: Copyright (C) 2024 Batmend Ganbaatar and authors of Flow.
See [NOTICE](./NOTICE) for attribution and a summary of what changed.

The original authors are not responsible for this fork.

## Preface

![Flow logo](logo@16.png) Flow is a free, open-source, and beautifully simple
expense tracker — built with a focus on great UX, works fully offline, and runs
seamlessly across platforms.

This fork keeps the core tracker (accounts, transactions, categories, budgets,
and stats) and removes Eny, in-app support/community pages, geographic tagging
and spending maps, and transaction attachments / camera / Markdown notes.

## Download

Build from source. Store listings below belong to the **original** Flow app,
not this fork.

[![Google Play Store](https://img.shields.io/badge/Google_Play_Store-original_Flow-f5ccff?logo=google-play&logoColor=white&style=for-the-badge)](https://play.google.com/store/apps/details?id=mn.flow.flow)
[![App Store](https://img.shields.io/badge/App_Store-original_Flow-f5ccff?logo=appstore&logoColor=white&style=for-the-badge)](https://apps.apple.com/mn/app/flow-expense-tracker/id6477741670)
[![Original GitHub](https://img.shields.io/badge/GitHub-flow--mn/flow-f5ccff?logo=github&logoColor=white&style=for-the-badge)](https://github.com/flow-mn/flow)

> You can build and run for Linux and macOS. Haven't tested Windows yet[^2]

## Features

* Simple UX helping you efficiently track your finances
* Infinite accounts and currencies (including various cryptos)
* Categories, tags
* Reflect on your spendings
* Fully-offline[^1]
* Full control over your data
  * No trackers, no analytics
  * Fully recoverable backups (ZIP/JSON)
  * Export CSV, PDFs
  * Periodic auto-backups to iCloud
* [URI-based automation](#uri-based-automation)

## URI-based automation

You can add one or more transactions using `flow-mn` schema uris.

Check out the supported [JSON Schema file in schemas folder](./schemas/programmable-object.json).

Currencies are based on the account, so there's no way to specify it at the moment.

### Adding single transaction

When adding single transactions, properties must be provided as query params.

```json
{
  "title": "Tous les jours",
  "amount": 42000.00
}
```

turns into:

```plain
flow-mn:///transaction/new?title=Tous+les+jours&amount=42000.00
```

### Adding multiple transactions

When adding multiple transactions, you must provide stringified version of the following as "json" query param.

```json
{
  "t": [
    {
      "title": "Fresh blueberry piece",
      "amount": "13000.00",
      "transactionDate": "2011-12-05",
      "category": "Food",
      "tags": "My fave cafe",
      "accountUuid": "faa6d523-277f-46af-9493-67768e5b48ab",
    },
    {
      "title": "Caffe Mocha ice",
      "amount": "10000.00",
      "transactionDate": "2011-12-05",
      "category": "Drinks"
    }
  ]
}
```

turns into

```plain
flow-mn:///transaction/new?json=%7B%22t%22%3A%5B%7B%22title%22%3A%22Fresh%20blueberry%20piece%22%2C%22amount%22%3A%2213000.00%22%2C%22transactionDate%22%3A%222011-12-05%22%2C%22category%22%3A%22Food%22%7D%2C%7B%22title%22%3A%22Caffe%20Mocha%20ice%22%2C%22amount%22%3A%2210000.00%22%2C%22transactionDate%22%3A%222011-12-05%22%2C%22category%22%3A%22Drinks%22%7D%5D%7D
```

## Development

Please read [Contribuition guide](./CONTRIBUTING.md), and
[Code of Conduct](./CODE_OF_CONDUCT.md) before contributing.

### Prerequisites

* [Flutter](https://flutter.dev/) (latest stable)

Other:

* JDK 11 or later if you're gonna build for Android
* [XCode](https://developer.apple.com/xcode/) if you're gonna build for iOS/macOS
* To run tests on your machine, see [Testing](#testing)

Building for Windows, macOS, and Linux-based systems requires the same
dependencies as Flutter. Read more on <https://docs.flutter.dev/platform-integration>

### Testing

If you plan to run tests on your machine, ensure you've installed ObjectBox
dynamic libraries.

Install ObjectBox dynamic libraries[^3]:

`bash <(curl -s https://raw.githubusercontent.com/objectbox/objectbox-dart/main/install.sh)`

Run tests with: `flutter test`

## Support the original Flow

This fork is independent. If you want to support the original project:

* Star [flow-mn/flow](https://github.com/flow-mn/flow)
* [Buy the original maintainer a coffee](https://buymeacoffee.com/sadespresso)

Thank you to all the original contributors, supporters, testers, and those who
contributed indirectly 🤍

## List of supported languages

* Arabic - thanks to [Ultrate](https://github.com/Ultrate)
* English
* French (France)
* German (Germany) - thanks to [MarkusWangler](https://github.com/MarkusWangler)
* Italian (Italy) - thanks to [albertorizzi](https://github.com/albertorizzi)
* Mongolian (Mongolia)
* Russian (Russia)
* Spanish (Spain)
* Turkish (Turkiye) - thanks to [NoRiskNoViski](https://github.com/NoRiskNoViski)
* Ukranian (Ukrain)
* Czech (Czechia) - thanks to **Miloš Koliáš** through email

> See [Translation guide](./CONTRIBUTING.md#translating) if you want to make
> Flow available to your language

<!-- markdownlint-disable-next-line -->
<!-- <a href="https://www.producthunt.com/posts/flow-2cbe921f-2ed9-4ed1-b8d7-26dff1c2c49d?embed=true&utm_source=badge-top-post-badge&utm_medium=badge&utm_souce=badge-flow&#0045;2cbe921f&#0045;2ed9&#0045;4ed1&#0045;b8d7&#0045;26dff1c2c49d" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/top-post-badge.svg?post_id=955354&theme=light&period=daily&t=1745222977391" alt="Flow - A&#0032;FOSS&#0032;expense&#0032;tracker&#0032;that&#0032;focuses&#0032;on&#0032;privacy&#0032;and&#0032;UX | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a> -->

[^1]: Flow requires internet to download currency exchage rates. Only necessary
if you use more than one currencies

[^2]: Will be available on macOS, Windows, and Linux-based systems, but no plan
to enhance the UI for desktop experience for now.

[^3]: Please double-check from the official website, may be outdated. Visit
<https://docs.objectbox.io/getting-started#add-objectbox-to-your-project>
(make sure to choose Flutter to see the script).
