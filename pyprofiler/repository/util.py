def features_from_profile(profile):
    features = []
    for server in profile['servers']:
        features.append(f"{server['proto']}-listen:{server['port']}")
    for client in profile['clients']:
        features.append(f"{client['proto']}:{client['dest']}:{client['port']}")

    if profile['name'] != 'Unknown Device':
        features.append(f"hostname:{profile['name']}")

    return features
