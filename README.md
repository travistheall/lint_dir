<h1>Check files for unused imports and unused packages in requirements.txt</h1>
<h3>Brute force very slow I'm sure</h3>
<div>
    <p>The requirements.txt for this is fake. I used it to check against</p>
    <p>You do need pandas and tqdm though to run this. requirements.txt</p>
</div>
<h3>Known limitation</h3>
<p>If the requirement name is different from the import values then it will be missed. See <b>scikit-learn and sklearn</b>. I don't have an answer to that.</p>
<h3>Steps</h3>
<ol>
    <li>cd /Users/yashbehal/projects/doorstep-django</li>
    <li>Remove what we just did
        <ol>
            <li>rm -rf pylinttest</li>
            <li>rm -rf lint_dir</li>
    </li>
    <li>Clone me into the dd repository
        <ul>
            <li>git clone https://github.com/travistheall/lint_dir</li>
        </ul>
    </li>
    <li>
        Run
        <ul>
            <li>python3 lint_dir/main.py</li>
        </ul>
    </li>
    <li>
    Creates 3 files
        <ol>
            <li>out.txt: The output of the pylint command</li>
            <li>not_in_requirements.csv: A csv file with all the packages that are used in the project, but not in requirements.txt</li>
            <ul>
                <li>math, os, project modules, ...</li>
            </ul>
            <li>requirements.csv: A csv file with all the packages from requirements.txt and 1 if used 0 if not</li>
        </ol>
    </li>
</ol>