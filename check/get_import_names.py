import os
import pandas as pd
from .find_my_site_packages import find_my_site_packages


def get_import_names():
    pkgs_dir = find_my_site_packages()
    pkg_dirs = os.listdir(pkgs_dir)

    import_names = []
    for pkg_dir in pkg_dirs:
        pkg_path = os.path.join(pkgs_dir, pkg_dir)
        if os.path.isdir(pkg_path):
            for pkg_contents in os.listdir(pkg_path):
                if pkg_contents == "top_level.txt":
                    top_level_file = os.path.join(pkg_path, "top_level.txt")
                    import_name = open(top_level_file, "r").readline().strip()
                    import_names.append([pkg_dir, import_name])

    import_names = pd.DataFrame(data=import_names, columns=['req', 'import_name'])
    # import_names.to_csv("import_names.csv", index=False)
    # import_names = pd.read_csv("import_names.csv")
    for index, row in import_names.iterrows():
        endings = ['.dist-info', '-py2.7.egg-info']
        row_ends_with = [e for e in endings if row['req'].endswith(e)]
        if len(row_ends_with) > 0:
            requirement = row['req'].replace(row_ends_with[0], "")
            requirement = requirement.replace('-', "==")
            requirement = requirement.replace('_', "-")
            import_names.at[index, 'req'] = requirement
        else:
            print("error with", row['req'])

    import_names[['req_name', 'req_version']] = import_names['req'].str.split('==', expand=True)
    import_names = import_names[['req_name', 'import_name']]
    import_names.set_index('req_name', inplace=True, drop=True)
    return import_names
