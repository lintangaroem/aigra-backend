def load_and_preprocess_data(file_path):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    df = pd.read_csv(file_path)

    print("Kolom tersedia di CSV:", df.columns.tolist())

    # Gunakan kolom sesuai CSV kamu
    X = df[['Suhu', 'Kelembaban', 'CO2 (MQ135)']]
    y = df['kategori']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test, scaler
