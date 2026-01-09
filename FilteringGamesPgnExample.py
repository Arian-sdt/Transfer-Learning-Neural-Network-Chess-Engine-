import chess.pgn

def filter_lichess_games(pgn_file, output_pgn, 
                        min_elo=2000,
                        max_elo=2500,
                        max_games=15000,
                        include_draws=False,
                        min_time_control=600):  # 600 seconds = 10 minutes (blitz)
    """Filter Lichess games for transfer learning
    
    min_time_control: minimum time per side in seconds
    - 180 = 3min+ (includes bullet)
    - 600 = 10min+ (blitz and above, excludes bullet)
    - 1800 = 30min+ (rapid and above)
    """
    count = 0
    filtered = 0
    print(f"Filtering {pgn_file} (elo_range={min_elo}-{max_elo}, min_time={min_time_control}s, max_games={max_games})...")
    
    with open(pgn_file, 'r', encoding='utf-8', errors='ignore') as pgn_file:
        with open(output_pgn, 'w') as out_file:
            while True:
                game = chess.pgn.read_game(pgn_file)
                if game is None:
                    break
                count += 1
                
                # Data from games
                try:
                    white_elo = int(game.headers.get('WhiteElo', 0))
                    black_elo = int(game.headers.get('BlackElo', 0))
                    result = game.headers.get('Result')
                    time_control = game.headers.get('TimeControl', '')
                    eco = game.headers.get('ECO', '')
                except (ValueError, AttributeError, TypeError):
                    continue
                
                # Parse time control (format: "minutes+increment")
                try:
                    if time_control and '+' in time_control:
                        time_per_side = int(time_control.split('+')[0])
                    else:
                        continue
                except (ValueError, IndexError):
                    continue
                
                # Filtering
                if white_elo < min_elo or white_elo > max_elo or black_elo < min_elo or black_elo > max_elo:
                    continue
                if time_per_side < min_time_control:
                    continue
                if not include_draws and result == '1/2-1/2':
                    continue
                if not eco:
                    continue
                
                # Check move count without converting to SAN
                move_count = 0
                for move in game.mainline_moves():
                    move_count += 1
                    if move_count >= 5:
                        break
                
                if move_count < 5:
                    continue
                
                out_file.write(str(game) + '\n\n')
                filtered += 1
                if max_games and filtered >= max_games:
                    break
                
                if count % 10000 == 0:
                    print(f"  Processed: {count:,} | Kept: {filtered:,}")
    
    print(f"\n✓ Filtered: {filtered:,} games saved to {output_pgn}\n")
    return output_pgn

# TO RUN - Blitz and above (excludes bullet)
filter_lichess_games(
    pgn_file='lichess_db_standard_rated_2014-07.pgn',
    output_pgn='lichess_filtered_2000-2200.pgn',
    min_elo=2000,
    max_elo=2500,
    max_games=15000,
    min_time_control=600  # 10 minutes minimum (blitz + classical)
)