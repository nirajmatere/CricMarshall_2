from collections import defaultdict
import os
import asyncio

# ----------- Step 1: Raw Info Data -----------
async def preprocess_all_files(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        if filename.endswith("_info.csv"):
            input_path = os.path.join(input_folder, filename)
            print("Input filename: ", input_path)
            try:
                with open(input_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                info_dict = await preprocess_data(lines)
                match_text = await format_summary(info_dict)

                output_path = os.path.join(output_folder, filename.replace("_info.csv", ".txt"))
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(match_text)

            except Exception as e:
                print(f"Error processing {filename}: {e}")
                pass

# ----------- Step 2: Parse into a structured dict -----------
async def preprocess_data(raw_info):
    info_dict = defaultdict(list)
    for line in raw_info:
        parts = line.strip().split(',')
        if len(parts) == 3:
            _, key, value = parts
            info_dict[key].append(value)
        elif len(parts) == 4 and parts[1] == "player":
            _, _, team, player = parts
            info_dict[f'player_{team}'].append(player)
        else:
            continue
    return info_dict

# ----------- Step 3: Format natural language summary -----------
async def format_summary(info):
    summary = []
    summary.append(f"Match {info.get('match_number', [''])[0]} of the {info.get('event', [''])[0]} ({info.get('season', [''])[0]} season).")
    
    dates = ", ".join(info.get('date', []))
    summary.append(f"Dates: {dates}.")
    
    city = info.get('city', [''])[0]
    venue = info.get('venue', [''])[0]
    summary.append(f"Venue: {venue}, {city}.")
    
    teams = info.get('team', [])
    if len(teams) == 2:
        summary.append(f"Teams: {teams[0]} vs {teams[1]}.")
    
    toss = info.get('toss_winner', [''])[0]
    toss_decision = info.get('toss_decision', [''])[0]
    if toss and toss_decision:
        summary.append(f"{toss} won the toss and chose to {toss_decision}.")
    
    winner = info.get('winner', [''])[0]

    wickets = info.get('winner_wickets', [''])[0]
    runs = info.get('winner_runs', [''])[0]
    if winner:
        if wickets:
            summary.append(f"{winner} won the match" + (f" by {wickets} wickets."))
        elif runs:
            summary.append(f"{winner} won the match by {runs} runs.")
        else:
            summary.append(f"{winner} won the match.")
    else:
        summary.append(f'No result of the match.')
    
    summary.append(f"Player of the match: {info.get('player_of_match', [''])[0]}.")
    
    umpires = ", ".join(info.get('umpire', []))
    if umpires:
        summary.append(f"Umpires: {umpires}.")
    
    tv_umpire = info.get('tv_umpire', [''])[0]
    referee = info.get('match_referee', [''])[0]
    if tv_umpire:
        summary.append(f"TV Umpire: {tv_umpire}.")
    if referee:
        summary.append(f"Match Referee: {referee}.")
    
    players_aus = ", ".join(info.get('player_Australia', []))
    players_eng = ", ".join(info.get('player_England', []))
    if players_aus:
        summary.append(f"Australia's playing XI: {players_aus}.")
    if players_eng:
        summary.append(f"England's playing XI: {players_eng}.")
    
    return "\n".join(summary)


async def main():
    folder_csv_info = "../dataset/csv_dataset/"
    folder_txt_info = "../dataset/match_info_text/"
    await preprocess_all_files(folder_csv_info, folder_txt_info)

if __name__ == "__main__":
    asyncio.run(main())