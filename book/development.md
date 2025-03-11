# Development

## Client Configuration

```sh
pip install figio
```

## Developer Configuration

From the `~/autotwin/figio` folder, create the virtual enivronment,

```sh
python -m venv .venv
source .venv/bin/activate       # bash
source .venv/bin/activate.fish  # fish shell
```

Install the code in editable form,

```sh
pip install -e .[dev]
```

## Manual Distribution

```sh
python -m build . --sdist  # source distribution
python -m build . --wheel
twine check dist/*
```

## Distribution

The distribution steps will tag the code state as a release version, with a semantic version number, build the code as a wheel file, and publish to the wheel file as a release to GitHub.

### Tag

View existing tags, if any:

```bash
git tag
```

Create a tag.  Tags can be *lightweight* or *annotated*.
Annotated tags are recommended since they store tagger name, email, date, and
message information.  Create an annotated tag:

```bash
# example of an annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"
```

Push the tag to repo

```bash
# example continued
git push origin v1.0.0
```

Verify the tag appears on the repo

### Build

Ensure that `setuptools` and `build` are installed:

```bash
pip install setuptools build
```

Navigate to the project directory, where the `pyproject.toml` file is located
and create a wheel distribution.

```bash
# generates a .whl file in the dist directory
python -m build --wheel
```

### Semantic Version Bump

Create `.github/workflows/bump.yml` as follows:

```yml
name: Bump
on:
  release:
    types: published
jobs:
  bump:
    runs-on: ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@v4
      - name: bump
        id: bump
        run: |
          # VERSION=$(cargo tree | grep automesh | cut -d " " -f 2 | cut -d "v" -f 2)
          VERSION=$(grep version pyproject.toml | cut -d '"' -f 2)
          MAJOR_MINOR=$(echo $VERSION | rev | cut -d "." -f 2- | rev)
          PATCH=$(echo $VERSION | rev | cut -d "." -f 1)
          BUMP=$(( $PATCH + 1))
          BUMPED_VERSION=$(echo $MAJOR_MINOR"."$BUMP)
          BUMP_BRANCH=$(echo "bump-$VERSION-to-$BUMPED_VERSION")
          echo "bump_branch=$BUMP_BRANCH" >> $GITHUB_OUTPUT
          sed -i "s/version = \"$VERSION\"/version = \"$BUMPED_VERSION\"/" pyproject.toml
          git config --global user.email "bump"
          git config --global user.name "bump"
          git add pyproject.toml
          git commit -m "Bumping version from $VERSION to $BUMPED_VERSION."
          git branch $BUMP_BRANCH
          git checkout $BUMP_BRANCH
          git push --set-upstream origin $BUMP_BRANCH
      - name: pr
        uses: rematocorp/open-pull-request-action@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          from-branch: ${{ steps.bump.outputs.bump_branch }}
          to-branch: ${{ github.event.repository.default_branch }}
          repository-owner: autotwin
          repository: ${{ github.event.repository.name }}
```
