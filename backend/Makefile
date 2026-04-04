sql:
	sqlacodegen_v2 postgresql+psycopg2://dp_pg_user:supersecret@localhost:5432/dp_db \
	--schemas projects,raw,bronze,silver,gold \
	--generator declarative > src/postgres/models.py \
	&& awk 'NF {p=1} p' src/postgres/models.py > src/postgres/models.py.tmp \
	&& mv src/postgres/models.py.tmp src/postgres/models.py \
	&& sed -i '' 's/Optional\[\(.*\)\]/\1 | None/g' src/postgres/models.py \
	&& sed -i '' 's/List\[/list[/g' src/postgres/models.py \
	&& sed -i '' '/^from typing import Optional$$/d' src/postgres/models.py \
	&& sed -i '' '/^from typing import List$$/d' src/postgres/models.py \
	&& sed -i '' '/^from sqlalchemy.orm.base import Mapped$$/d' src/postgres/models.py \
	&& sed -i '' \
		-e 's/ResourceMetadata2/__TMP_SILVER_RENAMED2__/g' \
		-e 's/ResourceMetadata1/__TMP_RAW_RENAMED__/g' \
		-e 's/ResourceMetadata_/__TMP_GOLD_RENAMED__/g' \
		-e 's/ResourceMetadata/BronzeResourceMetadata/g' \
		-e 's/__TMP_GOLD_RENAMED__/GoldResourceMetadata/g' \
		-e 's/__TMP_RAW_RENAMED__/RawResourceMetadata/g' \
		-e 's/__TMP_SILVER_RENAMED2__/SilverResourceMetadata/g' \
		-e 's/VersionLineage2/__TMP_GOLD_VERSIONLINEAGE__/g' \
		-e 's/VersionLineage1/__TMP_SILVER_VERSIONLINEAGE__/g' \
		-e 's/VersionLineage_/__TMP_BRONZE_VERSIONLINEAGE__/g' \
		-e 's/VersionLineage/RawVersionLineage/g' \
		-e 's/__TMP_BRONZE_VERSIONLINEAGE__/BronzeVersionLineage/g' \
		-e 's/__TMP_SILVER_VERSIONLINEAGE__/SilverVersionLineage/g' \
		-e 's/__TMP_GOLD_VERSIONLINEAGE__/GoldVersionLineage/g' src/postgres/models.py \
	&& sed -i '' 's/, Column//' src/postgres/models.py \
	&& uvx ruff format src/postgres/models.py \
	&& uvx ruff check --fix src/postgres/models.py