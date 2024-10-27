def timeline_analyzer(entries):
    """Analyze mental health progression over time"""
    if not entries:
        return []
    
    shifts = []
    for i in range(1, len(entries)):
        current = entries[i]
        previous = entries[i-1]
        
        shift = {
            'day': i + 1,
            'changes': [],
            'severity_trend': None,
            'overall_status': None
        }
        
        # Detect category changes
        if current['categories'] != previous['categories']:
            shift['changes'].append(f"Concern shifted from {previous['categories']} to {current['categories']}")
        
        # Detect intensity changes
        intensity_diff = float(current['intensities']) - float(previous['intensities'])
        if abs(intensity_diff) >= 2:
            trend = "increased" if intensity_diff > 0 else "decreased"
            shift['severity_trend'] = f"Severity {trend} by {abs(intensity_diff)} points"
        
        # Detect polarity changes
        if current['polarity'] != previous['polarity']:
            shift['changes'].append(f"Emotional state changed from {previous['polarity']} to {current['polarity']}")
        
        # Determine overall status
        if current['polarity'] == 'positive' and previous['polarity'] != 'positive':
            shift['overall_status'] = "Showing improvement"
        elif current['polarity'] == 'negative' and previous['polarity'] != 'negative':
            shift['overall_status'] = "Showing decline"
        elif float(current['intensities']) < float(previous['intensities']):
            shift['overall_status'] = "Gradually improving"
        
        if shift['changes'] or shift['severity_trend'] or shift['overall_status']:
            shifts.append(shift)
    
    return shifts