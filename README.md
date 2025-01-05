# Mangakalot Notification App 📢📚

Este é um aplicativo que monitora os favoritos do site **Mangakakalot** e notifica o usuário sempre que novos capítulos forem lançados. O projeto foi desenvolvido com **FastAPI, React Native e Selenium** para facilitar a leitura de mangás sem precisar verificar manualmente as atualizações.

## 🛠 Tecnologias Utilizadas

- **Python (FastAPI, Selenium)** → Para a API backend e scraping dos capítulos de mangá.
- **React Native (Expo, TypeScript)** → Para o aplicativo mobile que exibe notificações dos novos capítulos.
- **SQLite** → Para armazenamento local das notificações não lidas.
- **SQLAlchemy** → ORM utilizado para manipulação do banco de dados.

---

## 📌 Funcionalidades

✅ **Monitoramento Automático**: O bot acessa a página de favoritos do Manganato periodicamente para verificar novas atualizações.

✅ **Banco de Dados**: Notificações são armazenadas em um banco SQLite, permitindo controle sobre quais já foram lidas.

✅ **Notificações no App**: O usuário recebe uma notificação sempre que um novo capítulo for encontrado.

✅ **Abertura Direta do Capítulo**: Ao clicar na notificação, o aplicativo redireciona para a página do capítulo no navegador.

✅ **Marcar como Lido**: O usuário pode remover notificações da lista de não lidas.

---

## 🚀 Como Instalar e Usar

### 🔧 Configuração do Backend (FastAPI)

1. **Clone o repositório**:
   ```sh
   git clone https://github.com/KauaLima157/Mangakalot-Notification-App.git
   cd Mangakalot-Notification-App
   ```

2. **Crie um ambiente virtual (opcional, recomendado)**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure o Selenium e o ChromeDriver**:
   - Baixe o [ChromeDriver](https://chromedriver.chromium.org/downloads) compatível com sua versão do Google Chrome.
   - Substitua o caminho do ChromeDriver no arquivo `MangaNotic.py`:
     ```python
     chrome_service = Service("C:\\Users\\SeuUsuario\\Downloads\\chromedriver.exe")
     ```

5. **Execute a API FastAPI**:
   ```sh
   uvicorn Main:app --reload
   ```
   O servidor será iniciado em `http://127.0.0.1:8000`.

---

### 📱 Configuração do Frontend (React Native)

1. **Inicialize novo expo app**:
   ```sh
   npx create-expo-app@latest myApp
   ```

2. **Navegue pelo diretório**:
   ```sh
   cd myApp
   ```

3. **Execute o aplicativo**:
   ```sh
   npm start
   ```
   Isso abrirá o Metro Bundler no navegador. Você pode testar o app no seu celular escaneando o QR Code com o Expo Go.

---

## 🌐 Endpoints da API

- `POST /update-notifications` → Busca novos capítulos e os salva no banco.
- `GET /unread-notifications` → Retorna notificações não lidas.
- `PUT /mark-as-read/{id}` → Marca uma notificação como lida.

---

## 📝 Melhorias Futuras

- [ ] Melhorar o sistema de notificações para suportar push notifications no celular.
- [ ] Adicionar suporte para múltiplos sites de mangá além do Mangakakalot.
- [ ] Criar um painel web para gerenciamento das notificações.

---

## 💜 Licença

Este projeto é de código aberto e pode ser modificado conforme necessário.

📩 **Desenvolvido por [Kauã Lima](https://github.com/KauaLima157)**  
Se tiver sugestões ou quiser contribuir, fique à vontade para abrir um **Pull Request** ou **Issue**. 🚀


