import "package:flow/constants.dart";
import "package:flow/l10n/extensions.dart";
import "package:flow/prefs/local_preferences.dart";
import "package:flow/sync/import/sample_csv.dart";
import "package:flow/theme/theme.dart";
import "package:flow/utils/extensions/custom_popups.dart";
import "package:flow/utils/extensions/toast.dart";
import "package:flow/widgets/general/list_header.dart";
import "package:flow/widgets/general/spinner.dart";
import "package:flow/widgets/home/preferences/profile_card.dart";
import "package:flutter/material.dart";
import "package:go_router/go_router.dart";
import "package:logging/logging.dart";
import "package:material_symbols_icons_flow/symbols.dart";

final Logger _log = Logger("ProfileTab");

class ProfileTab extends StatefulWidget {
  const ProfileTab({super.key});

  @override
  State<ProfileTab> createState() => _ProfileTabState();
}

class _ProfileTabState extends State<ProfileTab> {
  bool _loadingSampleData = false;

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: .start,
        children: [
          const SizedBox(height: 24.0),
          const Center(child: ProfileCard()),
          const SizedBox(height: 24.0),
          ListTile(
            title: Text("tabs.stats.insights".t(context)),
            leading: const Icon(Symbols.insights_rounded),
            trailing: LocalPreferences().openedInsightsIndex.get()
                ? null
                : Badge(
                    label: Text("general.new".t(context)),
                    backgroundColor: context.colorScheme.primary,
                    textColor: context.colorScheme.onPrimary,
                  ),
            onTap: () {
              final entry = LocalPreferences().openedInsightsIndex;
              if (!entry.get()) {
                entry.set(true);
                setState(() {});
              }
              context.push("/stats/insights");
            },
          ),
          ListTile(
            title: Text("accounts".t(context)),
            leading: const Icon(Symbols.wallet_rounded),
            onTap: () => context.push("/accounts"),
          ),
          ListTile(
            title: Text("categories".t(context)),
            leading: const Icon(Symbols.category_rounded),
            onTap: () => context.push("/categories"),
          ),
          ListTile(
            title: Text("preferences.transactions.pending".t(context)),
            leading: const Icon(Symbols.search_activity_rounded),
            onTap: () => context.push("/transactions/pending"),
          ),
          const SizedBox(height: 32.0),
          ListHeader("tabs.profile.other".t(context)),
          ListTile(
            title: Text("transaction.deleted".t(context)),
            leading: const Icon(Symbols.delete_rounded),
            onTap: () => context.push("/transactions/deleted"),
          ),
          ListTile(
            title: Text("tabs.profile.backup".t(context)),
            leading: const Icon(Symbols.hard_drive_rounded),
            onTap: () => context.push("/exportOptions"),
          ),
          ListTile(
            title: Text("tabs.profile.import".t(context)),
            leading: const Icon(Symbols.restore_page_rounded),
            onTap: () => context.push("/import"),
          ),
          ListTile(
            title: Text("tabs.profile.loadSampleData".t(context)),
            leading: const Icon(Symbols.science_rounded),
            onTap: _loadingSampleData ? null : _loadSampleData,
          ),
          ListTile(
            title: Text("tabs.profile.preferences".t(context)),
            leading: const Icon(Symbols.settings_rounded),
            onTap: () => context.push("/preferences"),
          ),
          const SizedBox(height: 64.0),
          Center(
            child: Text("v$appVersion", style: context.textTheme.labelSmall),
          ),
          const SizedBox(height: 24.0),
          const SizedBox(height: 96.0),
        ],
      ),
    );
  }

  Future<void> _loadSampleData() async {
    if (_loadingSampleData) return;

    final bool? confirm = await context.showConfirmationSheet(
      title: "sync.import.eraseWarning".t(context),
      isDeletionConfirmation: true,
      mainActionLabelOverride: "general.confirm".t(context),
      child: Text(
        "tabs.profile.loadSampleData.eraseWarning".t(context),
        style: context.textTheme.bodyMedium?.copyWith(
          color: context.flowColors.expense,
        ),
        textAlign: TextAlign.center,
      ),
    );

    if (confirm != true || !mounted) return;

    setState(() => _loadingSampleData = true);
    _showLoadingDialog();

    try {
      await importSampleCsv();
      if (!mounted) return;
      _dismissLoadingDialog();
      context.showToast(text: "sync.import.success".t(context));
    } catch (e, stackTrace) {
      _log.severe("Failed to load sample data", e, stackTrace);
      if (!mounted) return;
      _dismissLoadingDialog();
      context.showErrorToast(error: e);
    } finally {
      if (mounted) {
        setState(() => _loadingSampleData = false);
      }
    }
  }

  void _showLoadingDialog() {
    showDialog<void>(
      context: context,
      barrierDismissible: false,
      builder: (context) =>
          const PopScope(canPop: false, child: Center(child: Spinner())),
    );
  }

  void _dismissLoadingDialog() {
    Navigator.of(context, rootNavigator: true).pop();
  }
}
