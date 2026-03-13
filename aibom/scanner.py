import ast
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Set

TORCHVISION_DATASET_CLASSES = {
    "CIFAR10", "CIFAR100", "MNIST", "FashionMNIST", "KMNIST", "EMNIST",
    "QMNIST", "FakeData", "COCO", "LSUN", "ImageFolder", "DatasetFolder",
    "ImageNet", "CelebA", "SVHN", "PhotoTour", "SBU", "Flickr",
    "VOCDetection", "VOCSegmentation", "Cityscapes", "SBDataset",
    "USPS", "Kinetics", "HMDB51", "UCF101", "STL10", "SEMEION",
    "Omniglot", "PCAM", "Country211", "DTD", "Food101", "OxfordIIITPet",
    "RenderedSST2", "StanfordCars", "Flowers102", "FER2013", "GTSRB",
    "Places365", "TinyImagenet", "INaturalist",
}

def scan_project(project_path: Path) -> Dict[str, Any]:
    """Scan a Python project for datasets, models, and APIs."""
    datasets = []
    models = []
    apis = []
    
    for py_file in project_path.rglob("*.py"):
        try:
            tree = ast.parse(py_file.read_text())
        except (SyntaxError, UnicodeDecodeError):
            continue
        
        visitor = DetectionVisitor(str(py_file.relative_to(project_path)))
        visitor.visit(tree)
        
        datasets.extend(visitor.datasets)
        models.extend(visitor.models)
        apis.extend(visitor.apis)
    
    return {
        "aibom_version": "0.1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "project_path": str(project_path),
        "datasets": datasets,
        "models": models,
        "apis": apis,
    }

class DetectionVisitor(ast.NodeVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.datasets = []
        self.models = []
        self.apis = []
        self.imports = {}  # alias -> full module
        self.imported_modules = set()  # full module names
    
    def _add_dataset(self, name: str, source: str, source_url: str = None, line: int = None):
        self.datasets.append({
            "name": name,
            "source": source,
            "source_url": source_url,
            "detected_in": f"{self.file_path}:{line}" if line else self.file_path,
        })
    
    def _add_model(self, name: str, provider: str, model_card_url: str = None, line: int = None):
        self.models.append({
            "name": name,
            "provider": provider,
            "model_card_url": model_card_url,
            "detected_in": f"{self.file_path}:{line}" if line else self.file_path,
        })
    
    def _add_api(self, provider: str, endpoint_pattern: str, line: int = None):
        self.apis.append({
            "provider": provider,
            "endpoint_pattern": endpoint_pattern,
            "detected_in": f"{self.file_path}:{line}" if line else self.file_path,
        })
    
    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imported_modules.add(alias.name)
            self._detect_framework_import(alias.name, node.lineno)
            if alias.asname:
                self.imports[alias.asname] = alias.name
            else:
                # For simple import, each top-level module part
                parts = alias.name.split('.')
                self.imports[parts[0]] = alias.name
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = node.module
        if not module:
            self.generic_visit(node)
            return
        self.imported_modules.add(module)
        self._detect_framework_import(module, node.lineno)
        for alias in node.names:
            full_name = f"{module}.{alias.name}" if alias.name != "*" else module
            self._detect_framework_import(full_name, node.lineno)
            if alias.asname:
                self.imports[alias.asname] = full_name
            else:
                self.imports[alias.name] = full_name
        self.generic_visit(node)
    
    def _resolve_name(self, node: ast.AST) -> Optional[str]:
        """Resolve an AST name node to its full import path if possible."""
        if isinstance(node, ast.Name):
            return self.imports.get(node.id, node.id)
        elif isinstance(node, ast.Attribute):
            # Recursively resolve the value
            value = self._resolve_name(node.value)
            if value is None:
                return None
            return f"{value}.{node.attr}"
        return None
    
    def _detect_framework_import(self, module_name: str, line: int):
        """Detect framework imports and add appropriate entries."""
        if module_name == "sklearn" or module_name.startswith("sklearn."):
            self._add_model("scikit-learn", "scikit-learn", line=line)
        elif module_name == "langchain" or module_name.startswith("langchain."):
            self._add_api("langchain", "langchain", line=line)
        elif module_name == "llama_index" or module_name.startswith("llama_index."):
            self._add_api("llamaindex", "llamaindex", line=line)
        elif module_name == "vertexai" or module_name.startswith("vertexai."):
            self._add_api("google-vertex-ai", "vertexai", line=line)
        elif module_name == "cohere" or module_name.startswith("cohere."):
            self._add_api("cohere", "cohere", line=line)
        elif module_name == "google.cloud.aiplatform" or "google.cloud.aiplatform" in module_name:
            self._add_api("google-vertex-ai", "aiplatform", line=line)
    
    def visit_Call(self, node: ast.Call):
        # Helper to extract a string literal from an AST node
        def get_string_arg(node, index=0):
            if index < len(node.args) and isinstance(node.args[index], ast.Constant):
                return str(node.args[index].value)
            return None
        
        # Detect load_dataset() calls (Hugging Face datasets)
        if isinstance(node.func, ast.Name) and node.func.id == "load_dataset":
            dataset_name = get_string_arg(node)
            if dataset_name:
                self._add_dataset(dataset_name, "huggingface", f"https://huggingface.co/datasets/{dataset_name}", node.lineno)
        
        # Detect from_pretrained() calls (Hugging Face models)
        elif isinstance(node.func, ast.Attribute) and node.func.attr == "from_pretrained":
            model_name = get_string_arg(node)
            if model_name:
                self._add_model(model_name, "huggingface", f"https://huggingface.co/{model_name}", node.lineno)
        
        # Detect tfds.load() calls
        elif isinstance(node.func, ast.Attribute) and node.func.attr == "load":
            # Check if the parent is tfds
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "tfds":
                dataset_name = get_string_arg(node)
                if dataset_name:
                    self._add_dataset(dataset_name, "tfds", f"https://www.tensorflow.org/datasets/catalog/{dataset_name}", node.lineno)
        
        # Detect torchvision.datasets.* class instantiation
        # Check if the call's function is a Name or Attribute that resolves to a torchvision dataset class
        func = node.func
        if isinstance(func, (ast.Name, ast.Attribute)):
            resolved = self._resolve_name(func)
            if resolved:
                # Check if it's a torchvision dataset class
                # Pattern: torchvision.datasets.CIFAR10 or datasets.CIFAR10 (if imported as from torchvision import datasets)
                if resolved.startswith("torchvision.datasets."):
                    class_name = resolved.split(".")[-1]
                    if class_name in TORCHVISION_DATASET_CLASSES:
                        self._add_dataset(class_name, "torchvision", f"https://pytorch.org/vision/stable/datasets.html#{class_name.lower()}", node.lineno)
                elif resolved.startswith("datasets.") and "torchvision" in self.imported_modules:
                    # Possibly from torchvision import datasets
                    class_name = resolved.split(".")[-1]
                    if class_name in TORCHVISION_DATASET_CLASSES:
                        self._add_dataset(class_name, "torchvision", f"https://pytorch.org/vision/stable/datasets.html#{class_name.lower()}", node.lineno)
        
        # Detect scikit-learn class instantiation
        if isinstance(func, (ast.Name, ast.Attribute)):
            resolved = self._resolve_name(func)
            if resolved and (resolved.startswith("sklearn.") or resolved.startswith("sklearn_")):
                self._add_model(resolved.split(".")[-1], "scikit-learn", line=node.lineno)

        # Detect Cohere API calls
        if isinstance(node.func, ast.Attribute) and node.func.attr in ("generate", "chat"):
            if "cohere" in self.imported_modules:
                self._add_api("cohere", f"cohere.{node.func.attr}", node.lineno)

        # Detect OpenAI API calls
        # Patterns:
        #   openai.ChatCompletion.create
        #   client.chat.completions.create
        #   openai.resources.chat.completions.Completions.create (new SDK)
        # We'll detect any call where the function attribute chain contains "openai" and "create"
        if isinstance(node.func, ast.Attribute):
            attr_chain = []
            n = node.func
            while isinstance(n, ast.Attribute):
                attr_chain.append(n.attr)
                n = n.value
            if isinstance(n, ast.Name):
                attr_chain.append(n.id)
            attr_chain.reverse()
            
            if "openai" in attr_chain and attr_chain[-1] == "create":
                self._add_api("openai", ".".join(attr_chain), node.lineno)
            elif "anthropic" in attr_chain and attr_chain[-1] == "create":
                self._add_api("anthropic", ".".join(attr_chain), node.lineno)
            # New OpenAI SDK: client.chat.completions.create()
            elif attr_chain[-3:] == ["chat", "completions", "create"] and "openai" in self.imported_modules:
                self._add_api("openai", "chat.completions.create", node.lineno)
                # Extract model= kwarg if present
                for kw in node.keywords:
                    if kw.arg == "model" and isinstance(kw.value, ast.Constant):
                        self._add_model(str(kw.value.value), "openai", None, node.lineno)
            # New Anthropic SDK: client.messages.create()
            elif attr_chain[-2:] == ["messages", "create"] and "anthropic" in self.imported_modules:
                self._add_api("anthropic", "messages.create", node.lineno)
                # Extract model= kwarg if present
                for kw in node.keywords:
                    if kw.arg == "model" and isinstance(kw.value, ast.Constant):
                        self._add_model(str(kw.value.value), "anthropic", None, node.lineno)
        
        self.generic_visit(node)