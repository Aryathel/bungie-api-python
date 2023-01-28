import os
from datetime import datetime

import asyncio

from marshmallow import ValidationError

from generated import BungieClientAsync


async def validate(table) -> None:
    start = datetime.now()
    count = await table.count()
    try:
        await table.validate()
        print(f'{int((datetime.now() - start).total_seconds()): >3}s {table.table_name} [{count}]: OK')
    except ValidationError as e:
        print(f'{int((datetime.now() - start).total_seconds()): >3}s {table.table_name} [{count}]: FAIL - {e}')


async def validate_manifest() -> None:
    client = BungieClientAsync(os.getenv('BUNGIE_API_KEY'))

    print('--- A --------------------------------------------------------')
    # DestinyAchievementDefinition?
    # DestinyActivityDefinition
    await validate(client.manifest.activities)
    # DestinyActivityGraphDefinition
    await validate(client.manifest.activity_graphs)
    # DestinyActivityModeDefinition
    await validate(client.manifest.activity_modes)
    # DestinyActivityModifierDefinition
    await validate(client.manifest.activity_modifiers)
    # DestinyActivityTypeDefinition
    await validate(client.manifest.activity_types)
    # DestinyArtifactDefinition
    await validate(client.manifest.artifacts)
    print('--- B --------------------------------------------------------')
    # DestinyBondDefinition?
    # DestinyBreakerTypeDefinition
    await validate(client.manifest.breaker_types)
    print('--- C --------------------------------------------------------')
    # DestinyChecklistDefinition
    await validate(client.manifest.checklists)
    # DestinyClassDefinition
    await validate(client.manifest.classes)
    # DestinyCollectibleDefinition
    await validate(client.manifest.collectibles)
    print('--- D --------------------------------------------------------')
    # DestinyDamageTypeDefinition
    await validate(client.manifest.damage_types)
    # DestinyDestinationDefinition
    await validate(client.manifest.destinations)
    print('--- E --------------------------------------------------------')
    # DestinyEnergyTypeDefinition
    await validate(client.manifest.energy_types)
    # DestinyEquipmentSlotDefinition
    await validate(client.manifest.equipment_slots)
    # DestinyEventCardDefinition
    await validate(client.manifest.event_cards)
    print('--- F --------------------------------------------------------')
    # DestinyFactionDefinition
    await validate(client.manifest.factions)
    print('--- G --------------------------------------------------------')
    # DestinyGenderDefinition
    await validate(client.manifest.genders)
    print('--- H --------------------------------------------------------')
    # DestinyHistoricalStatsDefinition
    await validate(client.manifest.historical_stats)
    print('--- I --------------------------------------------------------')
    # DestinyInventoryBucketDefinition
    await validate(client.manifest.inventory_buckets)
    # DestinyInventoryItemDefinition
    await validate(client.manifest.items)
    # DestinyItemCategoryDefinition
    await validate(client.manifest.item_categories)
    # DestinyItemTierTypeDefinition
    await validate(client.manifest.item_tier_types)
    print('--- L --------------------------------------------------------')
    # DestinyLocationDefinition
    await validate(client.manifest.locations)
    # DestinyLoreDefinition
    await validate(client.manifest.lore)
    print('--- M --------------------------------------------------------')
    # DestinyMaterialRequirementSetDefinition
    await validate(client.manifest.material_requirement_sets)
    # DestinyMedalTierDefinition
    await validate(client.manifest.medal_tiers)
    # DestinyMetricDefinition
    await validate(client.manifest.metrics)
    # DestinyMilestoneDefinition
    await validate(client.manifest.milestones)
    print('--- O --------------------------------------------------------')
    # DestinyObjectiveDefinition
    await validate(client.manifest.objectives)
    print('--- P --------------------------------------------------------')
    # DestinyPlaceDefinition
    await validate(client.manifest.places)
    # DestinyPlugSetDefinition
    await validate(client.manifest.plug_sets)
    # DestinyPowerCapDefinition
    await validate(client.manifest.power_caps)
    # DestinyPresentationNodeDefinition
    await validate(client.manifest.presentation_nodes)
    # DestinyProgressionDefinition
    await validate(client.manifest.progressions)
    # DestinyProgressionLevelRequirementDefinition
    await validate(client.manifest.progression_level_requirements)
    print('--- R --------------------------------------------------------')
    # DestinyRaceDefinition
    await validate(client.manifest.races)
    # DestinyRecordDefinition
    await validate(client.manifest.records)
    # DestinyReportReasonCategoryDefinition
    await validate(client.manifest.report_reason_categories)
    # DestinyRewardSourceDefinition
    await validate(client.manifest.reward_sources)
    print('--- S --------------------------------------------------------')
    # DestinySackRewardItemListDefinition?
    # DestinySandboxPatternDefinition
    await validate(client.manifest.sandbox_patterns)
    # DestinySandboxPerkDefinition
    await validate(client.manifest.sandbox_perks)
    # DestinySeasonDefinition
    await validate(client.manifest.seasons)
    # DestinySeasonPassDefinition
    await validate(client.manifest.season_passes)
    # DestinySocketCategoryDefinition
    await validate(client.manifest.socket_categories)
    # DestinySocketTypeDefinition
    await validate(client.manifest.socket_types)
    # DestinyStatDefinition
    await validate(client.manifest.stats)
    # DestinyStatGroupDefinition
    await validate(client.manifest.stat_groups)
    print('--- T --------------------------------------------------------')
    # DestinyTalentGridDefinition
    await validate(client.manifest.talents)
    # DestinyTraitCategoryDefinition
    await validate(client.manifest.trait_categories)
    # DestinyTraitDefinition
    await validate(client.manifest.traits)
    print('--- U --------------------------------------------------------')
    # DestinyUnlockDefinition
    await validate(client.manifest.unlocks)
    print('--- V --------------------------------------------------------')
    # DestinyVendorDefinition
    await validate(client.manifest.vendors)
    # DestinyVendorGroupDefinition
    await validate(client.manifest.vendor_groups)


async def main():
    client = BungieClientAsync(os.getenv('BUNGIE_API_KEY'))
    # await client.manifest.milestones.validate()
    res = await client.user.search_by_global_name_post(1, 'Ary')
    print([f'{n.bungieGlobalDisplayName}#{n.bungieGlobalDisplayNameCode}' for n in res.Response.searchResults])

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(validate_manifest())
    # loop.run_until_complete(main())
