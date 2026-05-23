if __name__ == "__main__":
    # Simulação rápida de teste
    from dotenv import load_dotenv
    load_dotenv() # Carrega o .env local

    # Substitua pelo seu e-mail de teste
    USER_EMAIL = "paragon.automations+ideas@gmail.com" 
    
    parser = EmailParser(USER_EMAIL)
    if parser.connect():
        print("Conectado com sucesso!")
        url = parser.get_latest_insta_url()
        if url:
            print(f"Resultado do teste: {url}")
        parser.logout()
    else:
        print("Falha na conexão. Verifique seu GMAIL_APP_PASSWORD.")