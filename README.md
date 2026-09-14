# ![Flow logo](logo@32.png) Flow (modified)

A simple personal finance tracker. This repository is a **modified version** of
[Flow](https://github.com/flow-mn/flow) (September 2026). It remains free
software under the [GNU General Public License v3](./LICENSE).

Original copyright: Copyright (C) 2024 Batmend Ganbaatar and authors of Flow.
See [NOTICE](./NOTICE) for attribution and a summary of what changed.

This is a personal project. The original authors are not responsible for it,
and it is not the Flow app listed on the App Store or Google Play.

## What this version is

Offline-first expense tracking: accounts, transactions, categories, and stats.
Build and run from source (macOS and Linux work; Windows is untested).

Compared with upstream Flow, this version drops Eny, in-app support/community
and IAP, maps and geo tagging, attachments / camera / Markdown notes, tags and
budgets from the UI, OS scheduled notifications, and store-publish workflows.
Existing backup data for those features is still imported.

## Features

* Simple UX for day-to-day tracking
* Multiple accounts and currencies (including various cryptos)
* Categories and spending stats
* Fully offline[^1]
* Your data stays on device
  * No trackers, no analytics
  * Recoverable backups (ZIP/JSON)
  * Export CSV and PDFs
  * Periodic auto-backups to iCloud (Apple platforms)
* [URI-based automation](#uri-based-automation)

## URI-based automation

You can add one or more transactions using `flow-mn` scheme URIs (unchanged
from upstream).

See the [JSON Schema in `schemas/`](./schemas/programmable-object.json).
Currency comes from the account; it cannot be set on the URI.

### Adding a single transaction

Properties go in query params.

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

Pass a stringified JSON object as the `json` query param.

```json
{
  "t": [
    {
      "title": "Fresh blueberry piece",
      "amount": "13000.00",
      "transactionDate": "2011-12-05",
      "category": "Food",
      "accountUuid": "faa6d523-277f-46af-9493-67768e5b48ab"
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

## Development

This is a personal fork. See [CONTRIBUTING.md](./CONTRIBUTING.md) if you still
want to open a pull request, and [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

### Prerequisites

* [Flutter](https://flutter.dev/) (latest stable)
* JDK 11 or later to build for Android
* [Xcode](https://developer.apple.com/xcode/) to build for iOS/macOS

Desktop builds need the same native deps as Flutter. See
<https://docs.flutter.dev/platform-integration>.

### Testing

Install ObjectBox dynamic libraries first[^2]:

```sh
bash <(curl -s https://raw.githubusercontent.com/objectbox/objectbox-dart/main/install.sh)
```

Then: `flutter test`

Web is not supported (ObjectBox).

## Original Flow

Upstream: [flow-mn/flow](https://github.com/flow-mn/flow).
To support the original maintainer:
[buymeacoffee.com/sadespresso](https://buymeacoffee.com/sadespresso).

Thanks to everyone who contributed translations, testing, and code to Flow.

## Languages

Translations come from upstream:

* Arabic — [Ultrate](https://github.com/Ultrate)
* English
* French (France)
* German (Germany) — [MarkusWangler](https://github.com/MarkusWangler)
* Italian (Italy) — [albertorizzi](https://github.com/albertorizzi)
* Mongolian (Mongolia)
* Russian (Russia)
* Spanish (Spain)
* Turkish (Türkiye) — [NoRiskNoViski](https://github.com/NoRiskNoViski)
* Ukrainian (Ukraine)
* Czech (Czechia) — Miloš Koliáš

[^1]: Internet is only needed to download exchange rates when you use more
than one currency.

[^2]: Confirm the current install steps at
<https://docs.objectbox.io/getting-started#add-objectbox-to-your-project>
(choose Flutter).
