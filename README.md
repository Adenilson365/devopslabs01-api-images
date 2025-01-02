## Api de imagens - Parte do projeto devopslabs
### 
### Laboratórios de DevOps com:
- ServiceMesh
- Pipeline de CICD 
- Observabilidade
- Infraestrutura como código
- Kubernetes
- Cloud GCP
- E mais abordagens relacionadas a cultura DevOps.

### Repositórios relacionados:
- [FrontEnd - devopslabs01](https://github.com/Adenilson365/devopslabs01-frontend)
- [BackEnd - Catalogo devopslabs01](https://github.com/Adenilson365/devopslabs01-serviceMesh)
- [Terraform - IAC](https://github.com/Adenilson365/devopslabs01-iac)
[Laboratório de ServiceMesh - ISTIO](https://github.com/Adenilson365/manifests) 
[Laboratório de observabilidade - Stack Grafana](https://github.com/Adenilson365/devopslabs02-observabilidade)


### Documentação:
- [Logging](https://docs.python.org/3/library/logging.html#logrecord-attributes)

### Como executar Localmente:
- Necessário ter o docker instalado [LINK](https://www.docker.com/)
```
docker compose up -d --build
```
### Como parar:
```
docker compose down
```

- Api será exposta no localhost:5001/get-images/id
    - id é o nome da imagem com extensão (imagen1.png)
- Front será exposto no localhost:5000
![front](./doc-assets/gui-exemplo.png)

## Requisitos kubernetes:
- Essa imagem é base para alguns laboratórios DevOps, para executá-la adicione os arquivos de configuração conforme o lab:
- **OBS: Se o o repositório estiver como privado, o lab ainda está em desenvolvimento**
[Laboratório de ServiceMesh - ISTIO](https://github.com/Adenilson365/manifests) 
[Laboratório de observabilidade - Stack Grafana](https://github.com/Adenilson365/devopslabs02-observabilidade) - Localmente basta executar o docker compose.


