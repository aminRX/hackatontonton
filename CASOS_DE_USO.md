# 📋 Casos de Uso del Sistema de Clasificación de Flujos

## 🎯 Descripción General

Este documento detalla casos de uso específicos para cada tipo de flujo y escenario del sistema de clasificación de experiencia web/app basado en geocercas, plusvalía y condiciones de red.

---

## 🏆 **FLOW PREMIUM** - Experiencia Premium

### 🎯 **Características:**
- **Condiciones**: WiFi + Alta plusvalía + Velocidad >15Mbps + Batería >30% + Cobertura WiFi >80%
- **Experiencia**: Máxima calidad, todas las funciones disponibles
- **Zonas**: Polanco, Condesa, Roma

### 📱 **Casos de Uso:**

#### **1. Usuario Ejecutivo en Polanco**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.4333&longitude=-99.2000&network_speed=25.0&battery_level=85.0&time_of_day=14"
```
**Escenario**: Ejecutivo en oficina corporativa de Polanco
- **Aplicación**: Plataforma de trading en tiempo real
- **Funciones**: Gráficos 4K, streaming de datos, videoconferencias HD
- **Experiencia**: Sin limitaciones, máxima calidad visual

#### **2. Turista en Condesa**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.4100&longitude=-99.1800&network_speed=20.0&battery_level=90.0&time_of_day=10"
```
**Escenario**: Turista en hotel boutique de Condesa
- **Aplicación**: App de reservas de restaurantes premium
- **Funciones**: Realidad aumentada, videos 360°, reservas instantáneas
- **Experiencia**: Navegación fluida, contenido multimedia completo

#### **3. Influencer en Roma**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=android&latitude=19.4200&longitude=-99.1600&network_speed=18.0&battery_level=75.0&time_of_day=16"
```
**Escenario**: Influencer en café de Roma
- **Aplicación**: App de redes sociales
- **Funciones**: Live streaming 4K, edición de video en tiempo real
- **Experiencia**: Transmisión sin interrupciones, calidad profesional

---

## ⭐ **FLOW ESTÁNDAR** - Experiencia Estándar

### 🎯 **Características:**
- **Condiciones**: WiFi + Velocidad >8Mbps + Batería >20%
- **Experiencia**: Calidad alta, mayoría de funciones disponibles
- **Zonas**: Centro Histórico, Coyoacán

### 📱 **Casos de Uso:**

#### **1. Estudiante en Centro Histórico**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=android&latitude=19.4326&longitude=-99.1332&network_speed=12.0&battery_level=60.0&time_of_day=9"
```
**Escenario**: Estudiante universitario en biblioteca del Centro Histórico
- **Aplicación**: Plataforma educativa
- **Funciones**: Videoconferencias HD, descarga de materiales, foros
- **Experiencia**: Funcionalidad completa con calidad aceptable

#### **2. Profesional en Coyoacán**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.3500&longitude=-99.1600&network_speed=10.0&battery_level=45.0&time_of_day=15"
```
**Escenario**: Profesional trabajando desde casa en Coyoacán
- **Aplicación**: Herramientas de productividad empresarial
- **Funciones**: Videollamadas, compartir pantalla, documentos colaborativos
- **Experiencia**: Trabajo eficiente sin limitaciones críticas

#### **3. Comerciante en Mercado**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=android&latitude=19.4326&longitude=-99.1332&network_speed=8.5&battery_level=35.0&time_of_day=11"
```
**Escenario**: Comerciante en mercado del Centro Histórico
- **Aplicación**: App de pagos móviles
- **Funciones**: Transacciones rápidas, escaneo de códigos QR
- **Experiencia**: Operaciones fluidas, sin retrasos

---

## 📱 **FLOW BÁSICA** - Experiencia Básica

### 🎯 **Características:**
- **Condiciones**: WiFi + Velocidad moderada
- **Experiencia**: Funcionalidad básica, optimizada para conexiones lentas
- **Zonas**: Iztapalapa, Gustavo Madero

### 📱 **Casos de Uso:**

#### **1. Usuario Residencial en Iztapalapa**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=android&latitude=19.3550&longitude=-99.0900&network_speed=6.0&battery_level=25.0&time_of_day=20"
```
**Escenario**: Usuario en casa en Iztapalapa
- **Aplicación**: App de entretenimiento
- **Funciones**: Streaming de video SD, redes sociales básicas
- **Experiencia**: Contenido accesible con calidad reducida

#### **2. Trabajador en Gustavo Madero**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=android&latitude=19.4800&longitude=-99.1100&network_speed=5.0&battery_level=20.0&time_of_day=7"
```
**Escenario**: Trabajador en fábrica de Gustavo Madero
- **Aplicación**: App de comunicación laboral
- **Funciones**: Mensajes de texto, notificaciones, reportes simples
- **Experiencia**: Comunicación esencial sin multimedia pesado

#### **3. Estudiante en Biblioteca Pública**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.3550&longitude=-99.0900&network_speed=4.0&battery_level=15.0&time_of_day=14"
```
**Escenario**: Estudiante en biblioteca pública de Iztapalapa
- **Aplicación**: Plataforma de investigación
- **Funciones**: Búsqueda de textos, descarga de PDFs
- **Experiencia**: Acceso a información sin contenido multimedia

---

## 🔋 **FLOW LIGERA** - Experiencia Ligera

### 🎯 **Características:**
- **Condiciones**: WiFi + Velocidad <5Mbps
- **Experiencia**: Versión minimalista, carga rápida
- **Zonas**: Tláhuac, Milpa Alta

### 📱 **Casos de Uso:**

#### **1. Agricultor en Milpa Alta**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=android&latitude=19.1900&longitude=-99.0200&network_speed=3.0&battery_level=10.0&time_of_day=6"
```
**Escenario**: Agricultor en campo de Milpa Alta
- **Aplicación**: App de información agrícola
- **Funciones**: Consulta de precios, pronóstico del tiempo
- **Experiencia**: Información esencial, sin imágenes pesadas

#### **2. Vendedor Ambulante en Tláhuac**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=android&latitude=19.2800&longitude=-99.0100&network_speed=2.5&battery_level=8.0&time_of_day=12"
```
**Escenario**: Vendedor ambulante en mercado de Tláhuac
- **Aplicación**: App de inventario simple
- **Funciones**: Lista de productos, precios básicos
- **Experiencia**: Interfaz minimalista, carga instantánea

#### **3. Usuario en Zona Rural**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.1900&longitude=-99.0200&network_speed=1.5&battery_level=5.0&time_of_day=18"
```
**Escenario**: Usuario en zona rural de Milpa Alta
- **Aplicación**: App de servicios básicos
- **Funciones**: Consulta de horarios, mensajes de texto
- **Experiencia**: Funcionalidad esencial, sin multimedia

---

## 📴 **FLOW OFFLINE** - Experiencia Offline

### 🎯 **Características:**
- **Condiciones**: Sin WiFi o velocidad <2Mbps
- **Experiencia**: Modo offline, contenido precargado
- **Zonas**: Cualquier zona con conexión muy limitada

### 📱 **Casos de Uso:**

#### **1. Usuario en Metro**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=false&device=android&latitude=19.4326&longitude=-99.1332&network_speed=0.5&battery_level=30.0&time_of_day=8"
```
**Escenario**: Usuario en metro del Centro Histórico
- **Aplicación**: App de noticias
- **Funciones**: Contenido precargado, lectura offline
- **Experiencia**: Acceso a información sin conexión

#### **2. Turista en Zona Sin Cobertura**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=false&device=ios&latitude=19.1900&longitude=-99.0200&network_speed=0.1&battery_level=15.0&time_of_day=10"
```
**Escenario**: Turista en zona rural de Milpa Alta
- **Aplicación**: App de navegación offline
- **Funciones**: Mapas descargados, rutas precargadas
- **Experiencia**: Navegación sin conexión a internet

#### **3. Emergencia en Zona Aislada**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=false&device=android&latitude=19.2800&longitude=-99.0100&network_speed=0.0&battery_level=5.0&time_of_day=22"
```
**Escenario**: Emergencia en zona aislada de Tláhuac
- **Aplicación**: App de emergencias
- **Funciones**: Información médica offline, números de emergencia
- **Experiencia**: Acceso a información crítica sin conexión

---

## 🔄 **COMPARACIÓN DE FLUJOS**

### 📊 **Ejemplo: Mismo Usuario en Diferentes Zonas**

#### **Usuario Ejecutivo - Diferentes Ubicaciones:**

**1. En Polanco (Premium):**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.4333&longitude=-99.2000&network_speed=25.0&battery_level=90.0&time_of_day=14"
```
- **Experiencia**: Videoconferencias 4K, streaming sin límites
- **Aplicación**: Plataforma de trading profesional

**2. En Centro Histórico (Estándar):**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.4326&longitude=-99.1332&network_speed=12.0&battery_level=90.0&time_of_day=14"
```
- **Experiencia**: Videoconferencias HD, funcionalidad completa
- **Aplicación**: Herramientas de productividad

**3. En Iztapalapa (Básica):**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.3550&longitude=-99.0900&network_speed=6.0&battery_level=90.0&time_of_day=14"
```
- **Experiencia**: Videoconferencias SD, funciones limitadas
- **Aplicación**: Comunicación básica

**4. En Milpa Alta (Offline):**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=false&device=ios&latitude=19.1900&longitude=-99.0200&network_speed=1.0&battery_level=90.0&time_of_day=14"
```
- **Experiencia**: Modo offline, contenido precargado
- **Aplicación**: Información local sin conexión

---

## 🎯 **CASOS DE USO ESPECÍFICOS POR INDUSTRIA**

### 🏥 **Salud**

#### **Flow Premium - Hospital Privado en Polanco:**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.4333&longitude=-99.2000&network_speed=30.0&battery_level=80.0&time_of_day=10"
```
- **Aplicación**: Telemedicina HD
- **Funciones**: Consultas 4K, análisis de imágenes médicas
- **Experiencia**: Diagnóstico remoto de alta precisión

#### **Flow Básica - Clínica en Iztapalapa:**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=android&latitude=19.3550&longitude=-99.0900&network_speed=5.0&battery_level=40.0&time_of_day=9"
```
- **Aplicación**: Registro de pacientes
- **Funciones**: Consultas básicas, historial médico
- **Experiencia**: Gestión esencial de pacientes

### 🏦 **Finanzas**

#### **Flow Premium - Banco en Condesa:**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.4100&longitude=-99.1800&network_speed=25.0&battery_level=85.0&time_of_day=11"
```
- **Aplicación**: Banca en línea premium
- **Funciones**: Trading en tiempo real, análisis financiero
- **Experiencia**: Operaciones financieras sin límites

#### **Flow Estándar - Sucursal en Centro Histórico:**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=android&latitude=19.4326&longitude=-99.1332&network_speed=10.0&battery_level=60.0&time_of_day=13"
```
- **Aplicación**: Banca móvil estándar
- **Funciones**: Transferencias, consulta de saldos
- **Experiencia**: Operaciones bancarias básicas

### 🎓 **Educación**

#### **Flow Premium - Universidad Privada en Roma:**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.4200&longitude=-99.1600&network_speed=20.0&battery_level=70.0&time_of_day=15"
```
- **Aplicación**: Plataforma educativa premium
- **Funciones**: Clases virtuales 4K, laboratorios remotos
- **Experiencia**: Educación de alta calidad

#### **Flow Básica - Escuela Pública en Iztapalapa:**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=android&latitude=19.3550&longitude=-99.0900&network_speed=4.0&battery_level=30.0&time_of_day=8"
```
- **Aplicación**: Plataforma educativa básica
- **Funciones**: Materiales de estudio, tareas
- **Experiencia**: Educación accesible

---

## 🔧 **CASOS DE USO TÉCNICOS**

### 📊 **Monitoreo de Red**

#### **Análisis de Cobertura por Zona:**
```bash
# Comparar cobertura entre zonas
curl "http://localhost:8000/advanced-flow/compare?wifi1=true&device1=android&lat1=19.4333&lon1=-99.2000&wifi2=true&device2=android&lat2=19.3550&lon2=-99.0900"
```

### 🎛️ **Optimización de Recursos**

#### **Ajuste Dinámico de Calidad:**
```bash
# Usuario con batería baja en zona premium
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.4333&longitude=-99.2000&network_speed=25.0&battery_level=10.0&time_of_day=14"
```

### 📈 **Análisis de Tendencias**

#### **Patrones de Uso por Hora:**
```bash
# Mañana en Polanco
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.4333&longitude=-99.2000&network_speed=25.0&battery_level=90.0&time_of_day=8"

# Noche en Polanco
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.4333&longitude=-99.2000&network_speed=25.0&battery_level=90.0&time_of_day=22"
```

---

## 🎯 **CONCLUSIONES**

### **Beneficios del Sistema:**

1. **Experiencia Personalizada**: Cada usuario recibe la experiencia óptima para sus condiciones
2. **Optimización de Recursos**: Uso eficiente de ancho de banda y batería
3. **Inclusión Digital**: Acceso a servicios en zonas con conectividad limitada
4. **Escalabilidad**: Sistema adaptable a diferentes tipos de usuarios y ubicaciones
5. **Monitoreo Inteligente**: Análisis en tiempo real de condiciones de red

### **Impacto en el Usuario:**

- **Zonas Premium**: Experiencia de lujo sin limitaciones
- **Zonas Estándar**: Funcionalidad completa con calidad aceptable
- **Zonas Básicas**: Acceso esencial a servicios digitales
- **Zonas Emergentes**: Inclusión digital en áreas de desarrollo
- **Modo Offline**: Continuidad de servicio sin conexión

Este sistema permite democratizar el acceso a servicios digitales de calidad, adaptándose a las realidades de conectividad y recursos de cada zona de la Ciudad de México. 🚀
