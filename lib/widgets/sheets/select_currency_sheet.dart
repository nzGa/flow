import "package:flow/data/currencies.dart";
import "package:flow/l10n/extensions.dart";
import "package:flow/theme/theme.dart";
import "package:flow/utils/utils.dart";
import "package:flow/widgets/general/modal_sheet.dart";
import "package:flutter/material.dart";
import "package:go_router/go_router.dart";

/// Pops with a valid [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217)
/// currency code [String]
class SelectCurrencySheet extends StatelessWidget {
  final String? currentlySelected;

  const SelectCurrencySheet({super.key, this.currentlySelected});

  @override
  Widget build(BuildContext context) {
    return ModalSheet.scrollable(
      title: Text("account.edit.selectCurrency".t(context)),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          for (final CurrencyData currency in kAppCurrencies)
            ListTile(
              selected: currentlySelected == currency.code,
              title: Text(currency.name),
              subtitle: Text(
                currency.country.titleCase(),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              trailing: Text(
                currency.code,
                style: context.textTheme.bodyLarge?.copyWith(
                  fontFeatures: [const FontFeature.tabularFigures()],
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              onTap: () => context.pop(currency.code),
            ),
        ],
      ),
    );
  }
}
