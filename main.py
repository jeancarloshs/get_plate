import matplotlib.pyplot as plt
import cv2

imagem = cv2.imread("placa.png")
imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
imagem_suavizada = cv2.blur(imagem_gray, (13,13))
_, imagem_limiarizada = cv2.threshold(imagem_suavizada, 120, 255, cv2.THRESH_BINARY)
contornos, _ = cv2.findContours(imagem_limiarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# _, contornos, _ = cv2.findContours(imagem_limiarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

imagem_contornos = imagem.copy()
cv2.drawContours(imagem_contornos, contornos, -1, (0,255,0), 3)
lista_roi = []
razao_placa = 40/13

for contorno in contornos:
  (x, y, w, h) = cv2.boundingRect(contorno)

  area = int(w) * int(h)
  # print("Area = " + str(area))

  if area > 40000:
    razao_cont = w/h

    if razao_cont >= (razao_placa - 0.50*razao_placa) and razao_cont <= (razao_placa + 0.50*razao_placa):
        cv2.rectangle(imagem_contornos, (x,y), (x+w, y+h), (0,255,0), 2)
        lista_roi.append(contorno)

for item in lista_roi:
    (x, y, w, h) = cv2.boundingRect(item)
    roi = imagem[y:y+h, x:x+w]

    plt.figure(figsize=(10,5))
    plt.imshow(roi)
    cv2.imwrite("roi.png", roi)
    # cv2.rectangle(imagem_contornos, (x,y), (x+w, y+h), (255,0,0), 2)
    # cv2.putText(imagem_contornos, "Placa", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)

plt.figure(figsize=(20,10))
# plt.imshow(imagem_limiarizada, cmap="gray")
plt.imshow(imagem_contornos)
# plt.title("Placa Mercosul Escala de Cinza")

print("Placas identificadas: " + str(len(lista_roi)))
print("Contornos encontrados "+ str(len(imagem_contornos)))
# plt.axis("off")  # Optional: hides the axis for a cleaner display
plt.show()

# plt.imshow('img', imagem)