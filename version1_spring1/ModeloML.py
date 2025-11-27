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
import os

# === CONFIGURACIÓN DE RUTA DE IMÁGENES ===
CARPETA_FIGURAS = Path(__file__).resolve().parent / "static" / "figuras"
CARPETA_FIGURAS.mkdir(parents=True, exist_ok=True)

# =========================================
# 1) CARGAR DATAFRAME df_modelo_ticket_alto
# =========================================
def cargar_df_modelo():
    script_dir = Path(__file__).resolve().parent
    ruta = script_dir / "df_modelo_ticket_alto.csv"
    print(f"📂 Cargando dataframe desde: {ruta}")

    df = pd.read_csv(ruta)
    print("Shape del dataframe:", df.shape)
    return df


# =========================================
# 2) PREPARAR DATOS PARA ML
# =========================================
def preparar_datos(df):
    cols_numericas = [
        "num_items",
        "num_lineas",
        "num_unique_products",
        "mes",
        "dia_semana",
        "antiguedad_cliente_dias",
    ]
    cols_categoricas = []
    if "medio_pago" in df.columns:
        cols_categoricas.append("medio_pago")
    if "ciudad" in df.columns:
        cols_categoricas.append("ciudad")

    columnas_utiles = cols_numericas + cols_categoricas + ["ticket_alto"]
    df_ml = df[columnas_utiles].dropna()
    df_ml = pd.get_dummies(df_ml, columns=cols_categoricas, drop_first=True)
    X = df_ml.drop("ticket_alto", axis=1)
    y = df_ml["ticket_alto"]
    return X, y


# =========================================
# 3) ENTRENAR Y GUARDAR FIGURAS
# =========================================
def entrenar_y_guardar_figuras(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    cmap_azul = plt.get_cmap("Blues")

    # --- Regresión Logística ---
    log_reg = LogisticRegression(max_iter=1000)
    log_reg.fit(X_train, y_train)
    y_pred_lr = log_reg.predict(X_test)
    acc_lr = accuracy_score(y_test, y_pred_lr)
    cm_lr = confusion_matrix(y_test, y_pred_lr)

    disp_lr = ConfusionMatrixDisplay(cm_lr)
    disp_lr.plot(values_format="d", cmap=cmap_azul)
    plt.title(f"Matriz de confusión - Regresión Logística (Acc: {acc_lr:.3f})")
    plt.tight_layout()
    plt.savefig(CARPETA_FIGURAS / "modelo_original_logistica.png", bbox_inches="tight")
    plt.close()

    # --- Árbol de Decisión ---
    tree = DecisionTreeClassifier(max_depth=4, random_state=42)
    tree.fit(X_train, y_train)
    y_pred_tree = tree.predict(X_test)
    acc_tree = accuracy_score(y_test, y_pred_tree)
    cm_tree = confusion_matrix(y_test, y_pred_tree)

    disp_tree = ConfusionMatrixDisplay(cm_tree)
    disp_tree.plot(values_format="d", cmap=cmap_azul)
    plt.title(f"Matriz de confusión - Árbol (Acc: {acc_tree:.3f})")
    plt.tight_layout()
    plt.savefig(CARPETA_FIGURAS / "modelo_original_arbol.png", bbox_inches="tight")
    plt.close()

    print("✅ Figuras guardadas en:", CARPETA_FIGURAS)
    return log_reg


# =========================================
# 4) FRONTERA DE DECISIÓN SIMPLE
# =========================================
def plot_decision_boundary_simple(df):
    feature_x = "num_items"
    feature_y = "num_unique_products"

    df_simple = df[[feature_x, feature_y, "ticket_alto"]].dropna().copy()
    X_simple = df_simple[[feature_x, feature_y]].values
    y_simple = df_simple["ticket_alto"].values

    model = LogisticRegression()
    model.fit(X_simple, y_simple)

    x_min, x_max = X_simple[:, 0].min() - 1, X_simple[:, 0].max() + 1
    y_min, y_max = X_simple[:, 1].min() - 1, X_simple[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    plt.contourf(xx, yy, Z, alpha=0.3, cmap="Blues")
    plt.scatter(X_simple[:, 0], X_simple[:, 1], c=y_simple, edgecolor="k")
    plt.xlabel("num_items")
    plt.ylabel("num_unique_products")
    plt.title("Frontera de decisión (modelo simple)")
    plt.tight_layout()
    plt.savefig(CARPETA_FIGURAS / "modelo_original_frontera.png", bbox_inches="tight")
    plt.close()


# =========================================
# MAIN
# =========================================
def main():
    df = cargar_df_modelo()
    X, y = preparar_datos(df)
    _ = entrenar_y_guardar_figuras(X, y)
    plot_decision_boundary_simple(df)


if __name__ == "__main__":
    main()
