import yaml

with open("infra_config/env.yaml") as f:
    env = yaml.safe_load(f)

paths = {
    "bronze": env["bronze_path"],
    "silver": env["silver_path"],
    "gold": env["gold_path"],
}

tables = {
    "retailer_stock": f"{env['schema']}.silver_retailer_stock",
    "retailer_customer": f"{env['schema']}.silver_retailer_customer",
    # Extend as needed
}
