import csv
import json

def extract_rallies(csv_path, output_json_path, fps=30):
    MIN_RALLY_DURATION = 2.0      # Минимальная длительность розыгрыша (сек)
    MERGE_GAP_SECONDS = 8.0       # Максимальный пропуск детекции мяча (сек)
    
    frames_data = []
    
    
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            frame_num = int(float(row['Frame']))
            visibility = int(float(row['Visibility']))
            x = float(row['X'])
            y = float(row['Y'])
            
            frames_data.append({
                'frame': frame_num, 
                'is_visible': visibility == 1,
                'x': x,
                'y': y
            })

    if not frames_data:
        return []

    #  мяч виден (GAME) не виден (NON_GAME)
    segments = []
    current_state = frames_data[0]['is_visible']
    start_frame = frames_data[0]['frame']

    for data in frames_data[1:]:
        if data['is_visible'] != current_state:
            segments.append({
                'state': current_state, 
                'start': start_frame, 
                'end': data['frame'] - 1
            })
            current_state = data['is_visible']
            start_frame = data['frame']

    
    segments.append({
        'state': current_state, 
        'start': start_frame, 
        'end': frames_data[-1]['frame']
    })

    
    rallies = []
    for seg in segments:
        if seg['state']: 
            duration_sec = (seg['end'] - seg['start']) / fps
            
            
            if duration_sec >= MIN_RALLY_DURATION:
                
                if rallies and (seg['start'] - rallies[-1]['end_frame']) / fps <= MERGE_GAP_SECONDS:
                    rallies[-1]['end_frame'] = seg['end']
                else:
                    rallies.append({'start_frame': seg['start'], 'end_frame': seg['end']})

    
    result = []
    for i, r in enumerate(rallies, start=1):
        result.append({
            "number": i,
            "start_time": round(r['start_frame'] / fps, 1),
            "end_time": round(r['end_frame'] / fps, 1),
            "start_frame": r['start_frame'],
            "end_frame": r['end_frame'],
            "serve_side": "unknown"
        })

    # Сохранение
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return result

if __name__ == "__main__":
    input_csv = "data/artifacts/1/dinamo/ball.csv" 
    output_json = "data/artifacts/1/rallies.json"
    
    
    found = extract_rallies(input_csv, output_json, fps=30)
    
    print(f"\nНайдено розыгрышей: {len(found)}")
    for r in found[:10]: 
        print(f"Розыгрыш {r['number']}: {r['start_time']}s -> {r['end_time']}s")