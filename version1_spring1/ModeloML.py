import pandas as pd
import numpy as np
from pathlib import Path

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

# =========================================
# 1) CARGAR DATAFRAME df_modelo_ticket_alto
# =========================================

def cargar_df_modelo():
    script_dir = Path(__file__).resolve().parent
    ruta = script_dir / "df_modelo_ticket_alto.csv"
    print(f"📂 Cargando dataframe desde: {ruta}")

    df = pd.read_csv(ruta)
    print("Shape del dataframe:", df.shape)
    print(df.head())
    return df


# =========================================
# 2) PREPARAR DATOS PARA ML (X, y)
# =========================================

def preparar_datos(df):
    """
    Usa solo variables disponibles al momento de la compra.
    IMPORTANTE: NO usa 'ticket_total' para evitar fuga de información.
    """
    print("\n==============================")
    print(" PREPARANDO DATOS PARA ML")
    print("==============================")

    # Columnas numéricas (sin ticket_total)
    cols_numericas = [
        "num_items",
        "num_lineas",
        "num_unique_products",
        "mes",
        "dia_semana",
        "antiguedad_cliente_dias",
    ]

    # Columnas categóricas (si existen)
    cols_categoricas = []
    if "medio_pago" in df.columns:
        cols_categoricas.append("medio_pago")
    if "ciudad" in df.columns:
        cols_categoricas.append("ciudad")

    print("Columnas numéricas usadas:", cols_numericas)
    print("Columnas categóricas usadas:", cols_categoricas)

    columnas_utiles = cols_numericas + cols_categoricas + ["ticket_alto"]
    df_ml = df[columnas_utiles].copy()

    # Sacamos filas con NaN
    df_ml = df_ml.dropna()
    print("Shape después de dropna:", df_ml.shape)

    # Dummies para categóricas
    df_ml = pd.get_dummies(df_ml, columns=cols_categoricas, drop_first=True)

    print("\nColumnas finales de X:")
    print([c for c in df_ml.columns if c != "ticket_alto"])

    X = df_ml.drop("ticket_alto", axis=1)
    y = df_ml["ticket_alto"]

    return X, y


# =========================================
# 3) ENTRENAR Y EVALUAR MODELOS + GRAFICAR
# =========================================

def entrenar_y_evaluar_modelos(X, y):
    print("\n==============================")
    print(" TRAIN / TEST SPLIT")
    print("==============================")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y
    )

    print("Tamaño X_train:", X_train.shape)
    print("Tamaño X_test :", X_test.shape)

    # Usamos un colormap azul/blanco
    cmap_azul = plt.cm.Blues

    # ---------- Regresión Logística ----------
    print("\n==============================")
    print(" REGRESIÓN LOGÍSTICA")
    print("==============================")

    log_reg = LogisticRegression(max_iter=1000)
    log_reg.fit(X_train, y_train)

    y_pred_lr = log_reg.predict(X_test)

    acc_lr = accuracy_score(y_test, y_pred_lr)
    print(f"Accuracy Regresión Logística: {acc_lr:.4f}")

    cm_lr = confusion_matrix(y_test, y_pred_lr)
    print("\nMatriz de confusión (Logística):")
    print(cm_lr)

    print("\nClassification report (Logística):")
    print(classification_report(y_test, y_pred_lr))

    # Matriz de confusión bonita (azules y blanco)
    plt.figure()
    disp_lr = ConfusionMatrixDisplay(confusion_matrix=cm_lr, display_labels=[0, 1])
    disp_lr.plot(values_format="d", cmap=cmap_azul, colorbar=True)
    plt.title("Matriz de confusión - Regresión Logística")
    plt.tight_layout()
    plt.show()

    # ---------- Árbol de Decisión ----------
    print("\n==============================")
    print(" ÁRBOL DE DECISIÓN")
    print("==============================")

    tree = DecisionTreeClassifier(max_depth=5, random_state=42)
    tree.fit(X_train, y_train)

    y_pred_tree = tree.predict(X_test)

    acc_tree = accuracy_score(y_test, y_pred_tree)
    print(f"Accuracy Árbol de Decisión: {acc_tree:.4f}")

    cm_tree = confusion_matrix(y_test, y_pred_tree)
    print("\nMatriz de confusión (Árbol):")
    print(cm_tree)

    print("\nClassification report (Árbol):")
    print(classification_report(y_test, y_pred_tree))

    # Matriz de confusión bonita (azules y blanco)
    plt.figure()
    disp_tree = ConfusionMatrixDisplay(confusion_matrix=cm_tree, display_labels=[0, 1])
    disp_tree.plot(values_format="d", cmap=cmap_azul, colorbar=True)
    plt.title("Matriz de confusión - Árbol de Decisión")
    plt.tight_layout()
    plt.show()

    return log_reg  # por si luego querés reutilizarlo


# =========================================
# 4) FRONTERA DE DECISIÓN SIMPLE (2 FEATURES)
# =========================================

def plot_decision_boundary_simple(df):
    """
    Dibuja una frontera de decisión usando SOLO:
      - num_items
      - num_unique_products

    Es una versión simple para visualizar (no es el modelo completo).
    """
    feature_x = "num_items"
    feature_y = "num_unique_products"

    df_simple = df[[feature_x, feature_y, "ticket_alto"]].dropna().copy()
    X_simple = df_simple[[feature_x, feature_y]].values
    y_simple = df_simple["ticket_alto"].values

    # Entrenamos una regresión logística simple con estas 2 variables
    model = LogisticRegression()
    model.fit(X_simple, y_simple)

    # Malla de puntos en el plano
    x_min, x_max = X_simple[:, 0].min() - 1, X_simple[:, 0].max() + 1
    y_min, y_max = X_simple[:, 1].min() - 1, X_simple[:, 1].max() + 1

    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 200),
        np.linspace(y_min, y_max, 200)
    )

    grid_points = np.c_[xx.ravel(), yy.ravel()]
    Z = model.predict(grid_points)
    Z = Z.reshape(xx.shape)

    # Gráfico con fondo azul/blanco
    plt.figure()
    plt.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.Blues)

    # Puntos reales
    plt.scatter(
        X_simple[y_simple == 0, 0],
        X_simple[y_simple == 0, 1],
        marker="o",
        label="Ticket normal (0)"
    )
    plt.scatter(
        X_simple[y_simple == 1, 0],
        X_simple[y_simple == 1, 1],
        marker="s",
        label="Ticket alto (1)"
    )

    # Nombres de ejes en ESPAÑOL
    plt.xlabel("Cantidad de ítems")
    plt.ylabel("Cantidad de productos distintos")
    plt.title("Frontera de decisión (ítems vs productos distintos)")
    plt.legend()
    plt.tight_layout()
    plt.show()


# =========================================
# 5) MAIN
# =========================================

def main():
    df = cargar_df_modelo()
    X, y = preparar_datos(df)
    _ = entrenar_y_evaluar_modelos(X, y)
    # Gráfico de frontera simple
    plot_decision_boundary_simple(df)


if __name__ == "__main__":
    main()
