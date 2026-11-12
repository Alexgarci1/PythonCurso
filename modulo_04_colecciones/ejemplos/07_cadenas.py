"""Módulo 4 - Ejemplo 7: manipulación de cadenas."""

texto = "  Programación en Python  "

print(repr(texto.strip()), repr(texto.lstrip()), repr(texto.rstrip()))
print(texto.strip().upper(), texto.strip().title())
print(texto.replace("Python", "Java").strip())
print("Python" in texto, texto.find("Python"), texto.find("Java"))
print(texto.strip()[:12], texto.strip()[-6:], texto.strip()[::-1])

# --- split y join
linea = "Ada;Lovelace;36;Londres"
campos = linea.split(";")
print(campos, " | ".join(campos))
print("uno  dos   tres".split(), "a,b,,c".split(","))
print("clave=valor=x".split("=", 1), "puerto=8080".partition("="))

nombre, apellido, edad, ciudad = campos
print(f"{apellido.upper()}, {nombre} ({int(edad)} años)")

# --- Limpiar una entrada «sucia»
entrada = "  ADA@Ejemplo.COM ; linus@ejemplo.com;; Grace@ejemplo.com  "
correos = [correo.strip().lower() for correo in entrada.split(";") if correo.strip()]
print(correos)

# --- Comprobaciones
for valor in ["12345", "abc", "abc123", "   ", ""]:
    print(repr(valor), valor.isdigit(), valor.isalpha(), valor.isalnum(), valor.isspace())

# --- Un informe: partes en una lista y join al final
precios = {"teclado": 45.0, "raton": 19.9, "monitor": 1189.0}
lineas = [f"{'Producto':<12}{'Precio':>10}", "-" * 22]
for producto, precio in precios.items():
    lineas.append(f"{producto:<12}{precio:>10,.2f}")
lineas.append("-" * 22)
lineas.append(f"{'TOTAL':<12}{sum(precios.values()):>10,.2f}")
print("\n".join(lineas))
print(f"{0.125:.1%} {42:05d} {'centrado':^20}|")
