#!/usr/bin/env python3
"""
Script de visualización del modelo de clasificación de calidad de conexión
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
from sklearn.model_selection import train_test_split
import pandas as pd

from app.ml_model import classifier
from app.models import DeviceType

# Configurar estilo de matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_visualization_data():
    """Crea datos para visualización"""
    # Generar datos de prueba
    test_cases = []
    predictions = []
    probabilities = []
    
    # Casos de prueba sistemáticos
    for wifi in [True, False]:
        for device in [DeviceType.ANDROID, DeviceType.IOS]:
            # Hacer predicción
            pred = classifier.predict(wifi, device.value)
            
            test_cases.append({
                'wifi': wifi,
                'device': device.value,
                'wifi_num': 1 if wifi else 0,
                'device_android': 1 if device.value == 'android' else 0,
                'device_ios': 1 if device.value == 'ios' else 0
            })
            
            predictions.append(1 if pred['flow_type'] == 'flow-1' else 0)
            probabilities.append(pred['confidence_score'])
    
    return pd.DataFrame(test_cases), predictions, probabilities

def plot_decision_boundary():
    """Visualiza las reglas de decisión del modelo"""
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Crear datos de prueba
    X, y, probs = create_visualization_data()
    
    # Gráfico 1: Distribución por WiFi y Dispositivo
    ax1 = axes[0]
    
    # Crear matriz de resultados
    results_matrix = np.array([
        [probs[0], probs[1]],  # WiFi=True: Android, iOS
        [probs[2], probs[3]]   # WiFi=False: Android, iOS
    ])
    
    # Crear heatmap
    sns.heatmap(results_matrix, 
                annot=True, 
                fmt='.3f',
                xticklabels=['Android', 'iOS'],
                yticklabels=['WiFi OFF', 'WiFi ON'],
                cmap='RdYlGn',
                ax=ax1)
    
    ax1.set_title('Score de Confianza por Combinación\n(WiFi + Dispositivo)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Tipo de Dispositivo', fontsize=12)
    ax1.set_ylabel('Estado WiFi', fontsize=12)
    
    # Gráfico 2: Distribución de predicciones
    ax2 = axes[1]
    
    # Crear datos para el gráfico de barras
    labels = ['WiFi ON + Android', 'WiFi ON + iOS', 'WiFi OFF + Android', 'WiFi OFF + iOS']
    colors = ['green' if pred == 1 else 'red' for pred in y]
    
    bars = ax2.bar(labels, probs, color=colors, alpha=0.7)
    ax2.set_title('Score de Confianza por Caso de Uso', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Confianza', fontsize=12)
    ax2.set_ylim(0, 1)
    
    # Agregar etiquetas de flujo
    for i, (bar, pred) in enumerate(zip(bars, y)):
        flow_text = 'FLOW-1' if pred == 1 else 'FLOW-2'
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                flow_text, ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('decision_boundary.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_model_performance():
    """Visualiza el rendimiento del modelo"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Generar datos de entrenamiento para evaluación
    X, y = classifier._create_training_data()
    X_scaled = classifier.scaler.transform(X)
    
    # Dividir en train/test para evaluación más realista
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
    
    # Re-entrenar para evaluación
    classifier.model.fit(X_train, y_train)
    y_pred = classifier.model.predict(X_test)
    y_pred_proba = classifier.model.predict_proba(X_test)[:, 1]
    
    # 1. Matriz de Confusión
    ax1 = axes[0, 0]
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax1)
    ax1.set_title('Matriz de Confusión', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Predicción', fontsize=12)
    ax1.set_ylabel('Valor Real', fontsize=12)
    ax1.set_xticklabels(['FLOW-2', 'FLOW-1'])
    ax1.set_yticklabels(['FLOW-2', 'FLOW-1'])
    
    # 2. Curva ROC
    ax2 = axes[0, 1]
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    
    ax2.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
    ax2.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    ax2.set_xlim([0.0, 1.0])
    ax2.set_ylim([0.0, 1.05])
    ax2.set_xlabel('False Positive Rate', fontsize=12)
    ax2.set_ylabel('True Positive Rate', fontsize=12)
    ax2.set_title('Curva ROC', fontsize=14, fontweight='bold')
    ax2.legend(loc="lower right")
    ax2.grid(True)
    
    # 3. Distribución de probabilidades
    ax3 = axes[1, 0]
    
    # Separar probabilidades por clase real
    prob_flow2 = y_pred_proba[y_test == 0]
    prob_flow1 = y_pred_proba[y_test == 1]
    
    ax3.hist(prob_flow2, bins=20, alpha=0.7, label='FLOW-2 (Real)', color='red')
    ax3.hist(prob_flow1, bins=20, alpha=0.7, label='FLOW-1 (Real)', color='green')
    ax3.set_xlabel('Probabilidad Predicha', fontsize=12)
    ax3.set_ylabel('Frecuencia', fontsize=12)
    ax3.set_title('Distribución de Probabilidades', fontsize=14, fontweight='bold')
    ax3.legend()
    ax3.grid(True)
    
    # 4. Métricas de rendimiento
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Calcular métricas
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # Crear tabla de métricas
    metrics_text = f"""
    MÉTRICAS DE RENDIMIENTO
    
    Accuracy:  {accuracy:.3f}
    Precision: {precision:.3f}
    Recall:    {recall:.3f}
    F1-Score:  {f1:.3f}
    AUC-ROC:   {roc_auc:.3f}
    
    INTERPRETACIÓN:
    • Accuracy: Porcentaje de predicciones correctas
    • Precision: De los predichos como FLOW-1, cuántos realmente son FLOW-1
    • Recall: De los reales FLOW-1, cuántos fueron predichos correctamente
    • F1-Score: Media armónica entre precision y recall
    """
    
    ax4.text(0.1, 0.9, metrics_text, transform=ax4.transAxes, fontsize=12,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('model_performance.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_feature_importance():
    """Visualiza la importancia de las características"""
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Obtener coeficientes del modelo
    coefficients = classifier.model.coef_[0]
    feature_names = ['WiFi', 'Android', 'iOS']
    
    # Gráfico 1: Coeficientes del modelo
    ax1 = axes[0]
    bars = ax1.bar(feature_names, coefficients, color=['skyblue', 'lightgreen', 'lightcoral'])
    ax1.set_title('Coeficientes del Modelo (Regresión Logística)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Coeficiente', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Agregar valores en las barras
    for bar, coef in zip(bars, coefficients):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{coef:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # Gráfico 2: Análisis de casos
    ax2 = axes[1]
    
    # Crear casos de ejemplo
    cases = [
        ('WiFi ON + Android', [1, 1, 0]),
        ('WiFi ON + iOS', [1, 0, 1]),
        ('WiFi OFF + Android', [0, 1, 0]),
        ('WiFi OFF + iOS', [0, 0, 1])
    ]
    
    case_names = [case[0] for case in cases]
    case_scores = []
    
    for case_name, features in cases:
        # Calcular score manualmente
        score = sum(coef * feat for coef, feat in zip(coefficients, features))
        case_scores.append(score)
    
    colors = ['green' if score > 0 else 'red' for score in case_scores]
    bars = ax2.bar(case_names, case_scores, color=colors, alpha=0.7)
    ax2.set_title('Score Lineal por Caso de Uso', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Score Lineal', fontsize=12)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax2.grid(True, alpha=0.3)
    
    # Agregar etiquetas
    for bar, score in zip(bars, case_scores):
        flow_text = 'FLOW-1' if score > 0 else 'FLOW-2'
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                flow_text, ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Función principal para generar todas las visualizaciones"""
    print("🎨 Generando visualizaciones del modelo de clasificación...")
    
    # Asegurar que el modelo esté entrenado
    if not classifier.is_trained:
        classifier.train()
    
    print("📊 1. Visualizando reglas de decisión...")
    plot_decision_boundary()
    
    print("📈 2. Analizando rendimiento del modelo...")
    plot_model_performance()
    
    print("🔍 3. Explorando importancia de características...")
    plot_feature_importance()
    
    print("✅ Visualizaciones completadas! Archivos guardados:")
    print("   - decision_boundary.png")
    print("   - model_performance.png") 
    print("   - feature_importance.png")

if __name__ == "__main__":
    main()
