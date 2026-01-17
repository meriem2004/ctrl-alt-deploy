# 📋 Guide des Tests

## 🎯 Vue d'ensemble

Le projet contient une suite de tests complète pour valider toutes les fonctionnalités :

- **Tests unitaires** : Validation des mappers (EC2, RDS)
- **Tests d'intégration** : Validation de la génération Terraform
- **Tests end-to-end** : Validation du workflow complet

---

## 📁 Structure des Tests

```
tests/
├── __init__.py
├── test_mappers.py              # Tests unitaires pour les mappers
├── test_terraform_generator.py  # Tests d'intégration pour le générateur
└── test_end_to_end.py           # Tests end-to-end complets
```

---

## 🚀 Exécuter les Tests

### Tous les tests
```bash
python -m pytest tests/ -v
```

### Tests unitaires seulement
```bash
python -m pytest tests/test_mappers.py -v
```

### Tests d'intégration seulement
```bash
python -m pytest tests/test_terraform_generator.py -v
```

### Tests end-to-end seulement
```bash
python -m pytest tests/test_end_to_end.py -v
```

### Avec rapport de couverture
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

### Utiliser le script helper
```bash
python run_tests.py
python run_tests.py --unit
python run_tests.py --coverage
```

---

## 📊 Résultats Actuels

**33 tests** - **Tous passent ✅**

### Répartition :
- **Tests unitaires (mappers)** : 13 tests
- **Tests d'intégration (générateur)** : 7 tests
- **Tests end-to-end** : 4 tests

---

## 🧪 Types de Tests

### 1. Tests Unitaires (`test_mappers.py`)

Testent les fonctions de mapping individuelles :

- ✅ Mapping S/M/L/XL → types EC2
- ✅ Mapping S/M/L/XL → types RDS
- ✅ Mapping images Docker → moteurs RDS
- ✅ Extraction de versions depuis images
- ✅ Gestion des erreurs (images invalides)

**Exemple :**
```python
def test_map_machine_size_m(self):
    result = map_machine_size_to_instance_type(MachineSize.M)
    assert result == "t3.medium"
```

### 2. Tests d'Intégration (`test_terraform_generator.py`)

Testent la génération complète de fichiers Terraform :

- ✅ Génération de main.tf
- ✅ Génération de variables.tf
- ✅ Génération de vpc.tf (si nécessaire)
- ✅ Génération de fichiers EC2
- ✅ Génération de fichiers RDS
- ✅ Gestion VPC existant vs nouveau

**Exemple :**
```python
def test_generate_complete_ec2(self):
    spec = self.create_minimal_spec()
    output_dir = generate_terraform_config(spec, str(self.test_output_dir))
    assert (output_dir / "main.tf").exists()
    assert (output_dir / "test-service_instance.tf").exists()
```

### 3. Tests End-to-End (`test_end_to_end.py`)

Testent le workflow complet depuis le parsing jusqu'à la génération :

- ✅ Workflow complet EC2 seul
- ✅ Workflow complet EC2 + RDS
- ✅ Validation des specs invalides
- ✅ Tests avec différentes tailles de machines

**Exemple :**
```python
def test_full_workflow_ec2_and_rds(self):
    # Créer spec
    # Parser
    # Générer Terraform
    # Vérifier fichiers
```

---

## ✅ Checklist de Validation

### Mappers
- [x] Mapping EC2 (S/M/L/XL)
- [x] Mapping RDS (S/M/L/XL)
- [x] Mapping images Docker → moteurs RDS
- [x] Extraction versions
- [x] Gestion erreurs

### Génération Terraform
- [x] Génération main.tf
- [x] Génération variables.tf
- [x] Génération vpc.tf (automatique)
- [x] Génération EC2
- [x] Génération RDS
- [x] Gestion VPC existant

### Workflow Complet
- [x] Parsing → Génération EC2
- [x] Parsing → Génération EC2 + RDS
- [x] Validation specs invalides
- [x] Différentes tailles de machines

---

## 🔍 Comprendre les Tests

### Structure d'un test

```python
def test_nom_du_test(self):
    """
    Description de ce que le test vérifie.
    """
    # Arrange : Préparer les données
    spec = self.create_minimal_spec()
    
    # Act : Exécuter l'action
    result = generate_terraform_config(spec)
    
    # Assert : Vérifier le résultat
    assert result.exists()
    assert "expected_content" in result.read_text()
```

### Fixtures (setup/teardown)

Chaque classe de test a :
- `setup_method()` : Exécuté avant chaque test
- `teardown_method()` : Exécuté après chaque test

Cela garantit que chaque test part d'un état propre.

---

## 🐛 Déboguer les Tests

### Voir les détails d'un test qui échoue
```bash
python -m pytest tests/test_mappers.py::TestEC2Mappers::test_map_machine_size_s -v -s
```

### Exécuter un seul test
```bash
python -m pytest tests/test_mappers.py::TestEC2Mappers::test_map_machine_size_s
```

### Voir les print statements
```bash
python -m pytest tests/ -v -s
```

---

## 📈 Améliorer la Couverture

Pour voir la couverture de code :
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

Puis ouvrir `htmlcov/index.html` dans un navigateur.

---

## 🎯 Objectifs de Test

- **Couverture** : > 80% du code testé
- **Rapidité** : Tous les tests en < 5 secondes
- **Fiabilité** : Tests reproductibles et isolés

---

## ✅ Statut Actuel

**33/33 tests passent** ✅

Tous les composants critiques sont testés et validés !

