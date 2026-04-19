-- ============================================================
-- House Maintenance Tracker — Squamish, BC
-- Seed Data: Full household device catalog
-- Source: Gemini camera walkthrough + web research, Apr 2026
--
-- HOW TO RUN:
--   1. Go to console.neon.tech → your project → SQL Editor
--   2. Paste this entire file and click Run
--   3. Verify with: SELECT name, category FROM devices ORDER BY category, name;
--
-- RE-SEEDING (drop everything and start fresh):
--   DELETE FROM devices;  -- cascades to service_types and schedules
--   Then re-run this file.
-- ============================================================

-- Safety check: abort if devices already exist
DO $$ BEGIN
  IF EXISTS (SELECT 1 FROM devices LIMIT 1) THEN
    RAISE EXCEPTION
      'devices table is not empty. To re-seed, first run: DELETE FROM devices;';
  END IF;
END $$;

DO $$
DECLARE
  -- Device ID variables
  d_fridge      INTEGER;
  d_dishwash    INTEGER;
  d_oven        INTEGER;
  d_espresso    INTEGER;
  d_dryer       INTEGER;
  d_washer      INTEGER;
  d_water_htr   INTEGER;
  d_faucets     INTEGER;
  d_toilets     INTEGER;
  d_vanee       INTEGER;
  d_stelpro     INTEGER;
  d_baseboards  INTEGER;
  d_bath_fan    INTEGER;
  d_smoke_co    INTEGER;
  d_ceiling_fan INTEGER;

  -- Reused for each service type INSERT
  st INTEGER;

BEGIN

-- ============================================================
-- KITCHEN APPLIANCES
-- ============================================================

  -- ── Main Fridge ─────────────────────────────────────────
  INSERT INTO devices (name, category, model, purchase_date, warranty_expiry, notes)
  VALUES (
    'Main Fridge', 'Kitchen Appliances', 'KitchenAid KRFC300ESS',
    '2021-03-28', '2026-03-28',
    'Located in main kitchen island/wall unit. Ensure 1" clearance on sides for airflow. Sealed system warranty until 2026-03-28.'
  ) RETURNING id INTO d_fridge;

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_fridge, 'Water Filter Replacement', 180, '["EDR4RXD1"]',
    'EveryDrop Filter 4 (EDR4RXD1). Reset the "Filter" light on touch panel after installation.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_fridge, st, 'Water Filter Replacement', '2026-06-03', 180);

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_fridge, 'Air Filter Replacement', 180, '["W10311524"]',
    'FreshFlow Air Filter (W10311524). Located in center-rear of fridge interior.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_fridge, st, 'Air Filter Replacement', '2026-06-03', 180);

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_fridge, 'Condenser Coil Cleaning', 365, '[]',
    'Vacuum with brush attachment. Coils at bottom — remove front kick-plate to access.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_fridge, st, 'Condenser Coil Cleaning', '2026-07-18', 365);

  -- ── Dishwasher ──────────────────────────────────────────
  INSERT INTO devices (name, category, model, purchase_date, warranty_expiry, notes)
  VALUES (
    'Dishwasher', 'Kitchen Appliances', 'KitchenAid KDTM404KPS',
    '2021-03-28', '2022-03-28',
    'Features FreeFlex third rack. High humidity: check door gasket for mold.'
  ) RETURNING id INTO d_dishwash;

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_dishwash, 'Filter Cleaning', 30, '[]',
    'Twist center cylinder counter-clockwise to remove. Manual rinse under tap. Also inspect door gasket for mold.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_dishwash, st, 'Filter Cleaning', '2026-05-03', 30);

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_dishwash, 'System Descaling', 90, '["Affresh W10282479"]',
    'Run Affresh Dishwasher Cleaner tablet on hottest cycle. Prevents bio-film buildup in drains.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_dishwash, st, 'System Descaling', '2026-05-19', 90);

  -- ── Wall Oven ────────────────────────────────────────────
  INSERT INTO devices (name, category, model, purchase_date, warranty_expiry, notes)
  VALUES (
    'Wall Oven', 'Kitchen Appliances', 'KitchenAid KOSE500ESS',
    '2021-03-28', '2022-03-28',
    'Convection model. Check door seal for brittleness. Avoid Self-Clean (high heat) to preserve control board longevity.'
  ) RETURNING id INTO d_oven;

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_oven, 'Steam Clean / Manual Wipe', 90, '[]',
    'Use steam clean cycle, then wipe interior. Avoid Self-Clean high-heat mode — risks control board failure.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_oven, st, 'Steam Clean / Manual Wipe', '2026-05-19', 90);

  -- ── Espresso Machine ────────────────────────────────────
  INSERT INTO devices (name, category, model, purchase_date, warranty_expiry, notes)
  VALUES (
    'Espresso Machine', 'Kitchen Appliances', 'Ascaso Steel Duo',
    '2021-03-28', '2023-03-28',
    'Solid brass group head. Use soft filtered water to extend descaling interval to 180 days.'
  ) RETURNING id INTO d_espresso;

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_espresso, 'Descaling Cycle', 90, '["Cafetto LOD Green Descaler"]',
    'Follow Ascaso descaling procedure. Using soft filtered water can extend this to 180 days.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_espresso, st, 'Descaling Cycle', '2026-05-19', 90);


-- ============================================================
-- LAUNDRY SYSTEMS
-- ============================================================

  -- ── Dryer ───────────────────────────────────────────────
  INSERT INTO devices (name, category, model, purchase_date, notes)
  VALUES (
    'Dryer', 'Laundry Systems', 'Whirlpool YWHD560CHW1',
    '2021-03-28',
    'Heat pump dryer. Clean lint screen after every load (habit). Secondary heat pump filter: clean every 5-10 cycles or when indicator light activates.'
  ) RETURNING id INTO d_dryer;

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_dryer, 'Heat Pump Filter Clean', 30, '["W11483547"]',
    'Secondary heat pump filter (part #W11483547). Clean every 5-10 cycles — check indicator light. More frequent than lint screen.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_dryer, st, 'Heat Pump Filter Clean', '2026-05-03', 30);

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_dryer, 'Moisture Sensor Cleaning', 180, '[]',
    'Wipe the two metal strips inside drum with rubbing alcohol. Ensures accurate drying times and prevents overdrying.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_dryer, st, 'Moisture Sensor Cleaning', '2026-06-03', 180);

  -- ── Washer ──────────────────────────────────────────────
  INSERT INTO devices (name, category, model, purchase_date, notes)
  VALUES (
    'Washer', 'Laundry Systems', 'Whirlpool (stacked)',
    '2021-03-28',
    'Stacked unit. High Squamish humidity: inspect door gasket for mold monthly during drum clean.'
  ) RETURNING id INTO d_washer;

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_washer, 'Drum Clean Cycle', 30, '["Affresh W10282479"]',
    'Run with Affresh tablet or bleach on hottest cycle. Inspect and wipe door gasket for mold at same time.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_washer, st, 'Drum Clean Cycle', '2026-05-03', 30);

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_washer, 'Drain Pump Filter Check', 180, '[]',
    'Located behind bottom front panel. Remove and check for debris (coins, lint). Rinse under tap.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_washer, st, 'Drain Pump Filter Check', '2026-06-03', 180);


-- ============================================================
-- PLUMBING & WATER
-- ============================================================

  -- ── Water Heater ────────────────────────────────────────
  INSERT INTO devices (name, category, model, notes)
  VALUES (
    'Water Heater', 'Plumbing & Water', 'Rheem (check unit label)',
    'Annual flushing critical — Squamish seasonal turbidity causes sediment buildup. Check manufacture sticker for age.'
  ) RETURNING id INTO d_water_htr;

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_water_htr, 'Flush Sediment & Test T&P Valve', 365, '[]',
    'Attach hose to drain valve, flush until water runs clear. Lift T&P valve briefly to confirm it opens freely.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_water_htr, st, 'Flush Sediment & Test T&P Valve', '2026-07-18', 365);

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_water_htr, 'Anode Rod Inspection', 730, '[]',
    'Every 2-3 years. Replace if less than 1/2 inch thick. Magnesium rod preferred for BC soft water. Critical for tank longevity.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_water_htr, st, 'Anode Rod Inspection', '2026-10-16', 730);

  -- ── Faucets ─────────────────────────────────────────────
  INSERT INTO devices (name, category, model, notes)
  VALUES (
    'Faucets', 'Plumbing & Water', 'Kitchen + Bathrooms',
    'Squamish water is soft — aerator maintenance is for flow maintenance, not heavy mineral buildup.'
  ) RETURNING id INTO d_faucets;

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_faucets, 'Aerator Soak & Clean', 180, '[]',
    'Unscrew aerators from all faucets. Soak 30 min in white vinegar. Rinse and reinstall. Maintains pressure and flow.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_faucets, st, 'Aerator Soak & Clean', '2026-06-03', 180);

  -- ── Toilets ─────────────────────────────────────────────
  INSERT INTO devices (name, category, notes)
  VALUES (
    'Toilets', 'Plumbing & Water',
    'All toilets. Check flappers and fill valves. Silent leaks can waste 200+ litres/day.'
  ) RETURNING id INTO d_toilets;

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_toilets, 'Silent Leak Dye Test', 365, '[]',
    'Add food coloring to tank. Wait 15 min without flushing. If color appears in bowl, flapper needs replacement (~$10 part).')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_toilets, st, 'Silent Leak Dye Test', '2026-07-18', 365);


-- ============================================================
-- SAFETY & ELECTRICAL
-- ============================================================

  -- ── vanEE Ventilation ───────────────────────────────────
  INSERT INTO devices (name, category, notes)
  VALUES (
    'vanEE Ventilation Control', 'Safety & Electrical',
    'Critical for moisture control in Squamish high-humidity climate. Keep on Smart or High mode in winter to prevent window condensation and mold.'
  ) RETURNING id INTO d_vanee;

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_vanee, 'Clean Intake Hood & Internal Filters', 90, '[]',
    'Every 3 months minimum in Squamish. Ensure core is not frosted in winter. Check intake hood for blockages.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_vanee, st, 'Clean Intake Hood & Internal Filters', '2026-05-19', 90);

  -- ── Stelpro Thermostats ─────────────────────────────────
  INSERT INTO devices (name, category, notes)
  VALUES (
    'Stelpro Thermostats', 'Safety & Electrical',
    'Electric baseboard thermostats. SAFETY: turn off breaker before cleaning. Do not use liquids on vents.'
  ) RETURNING id INTO d_stelpro;

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_stelpro, 'Vacuum Vents & Dust', 180, '[]',
    'Turn off breaker at panel first. Vacuum only — no liquids. Check for any burning smell when re-energized.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_stelpro, st, 'Vacuum Vents & Dust', '2026-06-03', 180);

  -- ── Electric Baseboards ──────────────────────────────────
  INSERT INTO devices (name, category, notes)
  VALUES (
    'Electric Baseboards', 'Safety & Electrical',
    'Dust buildup reduces efficiency and causes burning smell at start of heating season.'
  ) RETURNING id INTO d_baseboards;

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_baseboards, 'Vacuum Fins (Pre-Winter)', 365, '[]',
    'Do this before Oct heating season. Vacuum fins with brush attachment. Run briefly at low heat to confirm no burning smell.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_baseboards, st, 'Vacuum Fins (Pre-Winter)', '2026-09-01', 365);

  -- ── Bathroom Exhaust Fan ─────────────────────────────────
  INSERT INTO devices (name, category, notes)
  VALUES (
    'Bathroom Exhaust Fan', 'Safety & Electrical',
    'High humidity environment — mold in fan housing is a real risk. Annual deep clean is critical in Squamish.'
  ) RETURNING id INTO d_bath_fan;

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_bath_fan, 'Deep Clean Motor & Blades', 365, '[]',
    'Remove cover, vacuum housing interior, wipe blades with damp cloth. Prevents mold growth and motor strain.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_bath_fan, st, 'Deep Clean Motor & Blades', '2026-07-18', 365);

  -- ── Smoke & CO Detector ─────────────────────────────────
  INSERT INTO devices (name, category, model, notes)
  VALUES (
    'Smoke & CO Detector', 'Safety & Electrical', 'BRK',
    '2026 BC Regs: CO alarm required on every storey and near all sleeping areas. Check manufacture date on back — replace smoke detector after 10yr, CO after 7yr.'
  ) RETURNING id INTO d_smoke_co;

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_smoke_co, 'Monthly Test', 30, '[]',
    'Press and hold test button until alarm sounds. All units must respond. Replace batteries annually or at first low-battery chirp.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_smoke_co, st, 'Monthly Test', '2026-05-03', 30);

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_smoke_co, 'Battery Replacement', 365, '[]',
    'Replace all batteries annually. While doing this, confirm manufacture dates — smoke units expire at 10yr, CO units at 7yr.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_smoke_co, st, 'Battery Replacement', '2026-07-18', 365);

  -- ── Ceiling Fan ─────────────────────────────────────────
  INSERT INTO devices (name, category, notes)
  VALUES (
    'Ceiling Fan', 'Safety & Electrical',
    'Direction: CW (low speed) in winter pushes warm air down. CCW in summer for cooling breeze. Toggle switch on motor housing.'
  ) RETURNING id INTO d_ceiling_fan;

  INSERT INTO service_types (device_id, name, frequency_days, part_numbers, notes)
  VALUES (d_ceiling_fan, 'Blade Clean & Direction Switch', 180, '[]',
    'Slide pillowcase over each blade to wipe without dropping dust on furniture. Flip direction toggle on motor housing for season change.')
  RETURNING id INTO st;
  INSERT INTO schedules (device_id, service_type_id, task_description, next_due_date, frequency_days)
  VALUES (d_ceiling_fan, st, 'Blade Clean & Direction Switch', '2026-06-03', 180);

END $$;

-- ── Verify ──────────────────────────────────────────────────────────────────
SELECT
  d.name,
  d.category,
  d.model,
  COUNT(st.id) AS service_types,
  COUNT(sc.id) AS schedules
FROM devices d
LEFT JOIN service_types st ON st.device_id = d.id
LEFT JOIN schedules sc ON sc.device_id = d.id
GROUP BY d.id, d.name, d.category, d.model
ORDER BY d.category, d.name;
