import os
import pandas as pd
from .find_my_site_packages import find_my_site_packages


def get_import_names():
    """
    Static function to find the import names from the environment's site packages
    Example:
    requirement name: Pillow (pip install Pillow)
    import name: PIL (import PIL)
    :return: pandas dataframe with the requirement name and the import name
    """
    pkgs_dir = find_my_site_packages()
    pkg_dirs = os.listdir(pkgs_dir)

    import_names = []
    for pkg_dir in pkg_dirs:
        # Pillow-6.2.2.1-py2.7.egg-info, cryptography-3.3.2.dist-info, etc
        pkg_path = os.path.join(pkgs_dir, pkg_dir)
        if os.path.isdir(pkg_path):
            for pkg_contents in os.listdir(pkg_path):
                if pkg_contents == "top_level.txt":
                    top_level_file = os.path.join(pkg_path, "top_level.txt")
                    # PIL, _openssl, etc
                    import_name = open(top_level_file, "r").readline().strip()
                    import_names.append([pkg_dir, import_name])

    import_names = pd.DataFrame(data=import_names, columns=['req', 'import_name'])
    for index, row in import_names.iterrows():
        endings = [".dist-info", ".dist-info'", "-py2.7.egg-info"]
        # Pillow-6.2.2.1-py2.7.egg-info, cryptography-3.3.2.dist-info, etc
        row_ends_with = [e for e in endings if row['req'].endswith(e)]
        if len(row_ends_with) > 0:
            # Pillow-6.2.2.1, cryptography-3.3.2, etc
            requirement = row['req'].replace(row_ends_with[0], "")
            requirement = requirement.replace('-', "==")
            requirement = requirement.replace('_', "-")
            # Pillow==6.2.2.1, cryptography==3.3.2, etc
            import_names.at[index, 'req'] = requirement
        else:
            print("error with", row['req'])

    import_names[['req_name', 'req_version']] = import_names['req'].str.split('==', expand=True)
    import_names = import_names[['req_name', 'import_name']]
    # req_name | import_name
    # --------------------------
    # Pillow     |  PIL
    # cryptography| cryptography
    import_names.set_index('req_name', inplace=True, drop=True)
    return import_names
