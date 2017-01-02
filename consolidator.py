import re;

f = open('../WarframeData/MissionDecks.txt', 'r');
fileString = f.read();

regex = re.compile('\[.*?\].*?\n\n\n', re.DOTALL);
tokens = regex.findall(fileString);
# tokens = re.search('\[.*?\].*?\n\n', fileString);

results = []
for token in tokens:
  result = {}
  lines = token.split('\n');
  result['name'] = lines[0];

  regex = re.compile('-.*')
  locations = regex.findall(token)
  result['locations'] = locations

  if "VoidKey" in result['name']:
    continue
  if "Sortie" in result['name']:
    continue
  if "Quest" in result['name']:
    continue

  regex = re.compile('Rotation .:.*?\n\n', re.DOTALL);
  rotations = regex.findall(token);
  if len(rotations) > 0:
    for rotation in rotations:
      lines = rotation.split('\n')

      rewards = {}
      rewards['endoAmount'] = 0
      rewards['endoChance'] = 0
      rewards['creditAmount'] = 0
      rewards['creditChance'] = 0
      rewards['blueprints'] = []
      rewards['blueprintChance'] = 0
      rewards['relics'] = []
      rewards['relicChance'] = 0
      rewards['mods'] = []
      rewards['modChance'] = 0
      for line in lines:
        if "  " not in line or "%" not in line:
          continue
        amount = reduce(lambda x, y: x*y, [int(s) for s in line.split() if s.isdigit()])
        regex = re.compile('[0-9]+\.*[0-9]*%')
        chance = regex.findall(line)
        chance = float(chance[0].strip('%'))
        if "ENDO" in line:
          oldChance = rewards['endoChance']
          rewards['endoChance'] = oldChance + chance
          rewards['endoAmount'] = (chance * amount + rewards['endoAmount'] * oldChance) / rewards['endoChance']
        elif "CREDITS" in line:
          oldChance = rewards['creditChance']
          rewards['creditChance'] = oldChance + chance
          rewards['creditAmount'] = (chance * amount + rewards['creditAmount'] * oldChance) / rewards['creditChance']
        elif "BLUEPRINT" in line:
          regex = re.compile('1.*BLUEPRINT')
          bpName = regex.findall(line)
          rewards['blueprints'].append(bpName[0])
          rewards['blueprintChance'] = rewards['blueprintChance'] + chance
        elif "RELIC" in line:
          regex = re.compile('1.*RELIC')
          bpName = regex.findall(line)
          rewards['relics'].append(bpName[0])
          rewards['relicChance'] = rewards['relicChance'] + chance
        else:
          regex = re.compile('[0-9].*?,')
          modName = regex.findall(line)[0].strip('1 ').strip(',')
          rewards['mods'].append(modName)
          rewards['modChance'] = rewards['modChance'] + chance

      result[lines[0]] = rewards

  else:
    continue

  results.append(result)

for result in results:
  print('\n')
  print(result['name'])
  for location in result['locations']:
    print(location)
  for key, elem in result.items():
    if "Rotation" in key:
      print('\n')
      print(key)
      print('Endo Chance: {} (average per drop: {}, per run: {})'.format(elem['endoChance'], elem['endoAmount'], elem['endoChance'] * elem['endoAmount'] / 100.0))
      print('Credit Chance: {} (average per drop: {}, per run: {})'.format(elem['creditChance'], elem['creditAmount'], elem['creditChance'] * elem['creditAmount'] / 100.0))
      print('Blueprint Chance: {} (types: {})'.format(elem['blueprintChance'], elem['blueprints']))
      print('Relic Chance: {} (types: {})'.format(elem['relicChance'], elem['relics']))
      print('Mod Chance: {} (types: {})'.format(elem['modChance'], elem['mods']))

f.close();

