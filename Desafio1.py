import requests
import json
import re
 
def obter_classe_gramatical_dicio(palavra):
    """Obtém a classe gramatical usando a API do Dicio"""
    url = f"https://www.dicio.com.br/api/v2/words/{palavra.lower()}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if 'partOfSpeech' in data:
                classe = data['partOfSpeech'].lower()
                if 'adv' in classe:
                    return "advérbio"
                elif 'prep' in classe:
                    return "preposição"
                else:
                    return classe
    except Exception as e:
        pass
   
    # Segunda tentativa com site alternativo
    try:
        url = f"https://api.dicionario-aberto.net/word/{palavra.lower()}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                if 'word' in entry:
                    xml_data = entry.get('xml', '')
                    if 'adv' in xml_data:
                        return "advérbio"
                    elif 'prep' in xml_data:
                        return "preposição"
    except:
        pass
   
    return None
 
def identificar_adjuntos(texto):
    palavras = texto.split()
    adjuntos = []
   
    for i, palavra in enumerate(palavras):
        palavra_limpa = re.sub(r'[^\w\s]', '', palavra.lower())
        if not palavra_limpa:
            continue
           
        classe = obter_classe_gramatical_dicio(palavra_limpa)
       
        if classe == "advérbio":
            adjuntos.append((palavra, "Advérbio"))
       
        elif classe == "preposição" and i < len(palavras) - 1:
            # Captura o sintagma preposicional
            j = i + 1
            sintagma = [palavra]
           
            while j < len(palavras):
                palavra_seguinte = palavras[j]
                classe_seguinte = obter_classe_gramatical_dicio(re.sub(r'[^\w\s]', '', palavra_seguinte.lower()))
               
                if classe_seguinte in ["verbo", "conjunção"]:
                    break
                   
                sintagma.append(palavra_seguinte)
                j += 1
           
            if len(sintagma) > 1:
                adjuntos.append((" ".join(sintagma), "Sintagma Preposicional"))
   
    return adjuntos
 
def main():
    print("Identificador de Adjuntos Adverbiais e Sintagmas Preposicionais")
    print("Digite o texto para análise:")
    texto = input(">> ")
   
    if not texto.strip():
        print("Texto vazio. Por favor, forneça um texto para análise.")
        return
   
    print("\nAnalisando o texto (isso pode levar alguns segundos)...")
    adjuntos = identificar_adjuntos(texto)
   
    if adjuntos:
        # Separar adjuntos por tipo
        adverbios = [adj[0] for adj in adjuntos if adj[1] == "Advérbio"]
        sintagmas = [adj[0] for adj in adjuntos if adj[1] == "Sintagma Preposicional"]
       
        print("\n== ADJUNTOS ENCONTRADOS ==")
       
        print("\nAdvérbios:")
        if adverbios:
            for adv in adverbios:
                print(f"- {adv}")
        else:
            print("- Nenhum advérbio encontrado.")
           
        print("\nSintagmas Preposicionais:")
        if sintagmas:
            for sint in sintagmas:
                print(f"- {sint}")
        else:
            print("- Nenhum sintagma preposicional encontrado.")
    else:
        print("\nNenhum adjunto encontrado no texto fornecido.")
 
if __name__ == "__main__":
    main()
 
#define TRIG_PIN 14
#define ECHO_PIN 27
#define NUM_COLETAS 100
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}
 
void loop() {
  float distancias[NUM_COLETAS];  // Array para armazenar as medições
 
  // Coletando os valores
  for (int i = 0; i < NUM_COLETAS; i++) {
    // Gera um pulso no Trig
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
 
    // Mede o tempo do eco
    long duration = pulseIn(ECHO_PIN, HIGH);
 
    // Converte para distância em cm e armazena no array
    distancias[i] = duration * 0.034 / 2;
 
    delay(10); // Pequeno atraso entre coletas
  }
 
  // Ordenação do array (Selection Sort)
  for (int i = 0; i < NUM_COLETAS - 1; i++) {
    int menorIndice = i;
    for (int j = i + 1; j < NUM_COLETAS; j++) {
      if (distancias[j] < distancias[menorIndice]) {
        menorIndice = j;
      }
    }
    // Troca os valores
    float temp = distancias[i];
    distancias[i] = distancias[menorIndice];
    distancias[menorIndice] = temp;
  }
 
  // Calcula a mediana
  float mediana;
  if (NUM_COLETAS % 2 == 0) {
    mediana = (distancias[NUM_COLETAS / 2 - 1] + distancias[NUM_COLETAS / 2]) / 2.0;
  } else {
    mediana = distancias[NUM_COLETAS / 2];
  }
 
  // Exibe os valores ordenados
  Serial.println("Valores coletados (ordenados):");
  for (int i = 0; i < NUM_COLETAS; i++) {
    Serial.print(distancias[i]);
    Serial.print(" cm, ");
  }
  Serial.println();
 
  // Exibe a mediana
  Serial.print("Mediana: ");
  Serial.print(mediana);
  Serial.println(" cm");
 
  delay(1000); // Aguarda antes da próxima medição
}
 