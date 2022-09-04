import pystac
import pandas as pd
from shapely.geometry import mapping, box
from datetime import datetime
import pytz


if __name__ == "__main__":

    # mapping for generating STAC Asset URLs
    prefix_mapping = {
        "DSM_5m": "R5",
        "DTM_5m": "M5",
        "DSM_0.5m": "R",
        "DTM_0.5m": "M",
        "point_cloud": "C",
    }

    bounds_csv_path = "resources/ahn3_tile_bounds.csv"
    # Initialize the catalog
    catalog = pystac.Catalog(
        id="AHN3 DSM 0.5m catalog",
        description="Catalog containing all AHN3 0.5m DSM tifs items.",
    )

    csv = pd.read_csv(bounds_csv_path)
    for i in range(len(csv)):
        row = csv.iloc[i]
        geom = box(row.left, row.bottom, row.right, row.top)
        bbox = geom.bounds
        id = row.tile_name

        # no metadata about acqusition datetime available.
        # But this entire dataset was collected from 2015 to 2019
        start_datetime = str(datetime(2015, 1, 1).astimezone(pytz.UTC))
        end_datetime = str(datetime(2019, 12, 31).astimezone(pytz.UTC))
        item = pystac.Item(
            id=id,
            geometry=mapping(geom),
            bbox=bbox,
            datetime=None,
            properties={
                "start_datetime": start_datetime,
                "end_datetime": end_datetime,
                "CRS": 28992,
            },
        )

        catalog.add_item(item)
        prefix = prefix_mapping["DSM_0.5m"]
        img_path = f"https://download.pdok.nl/rws/ahn3/v1_0/5m_dsm/{prefix}_{id}.ZIP"
        item.add_asset(
            key="image",
            asset=pystac.Asset(href=img_path, media_type=pystac.MediaType.GEOTIFF),
        )

    catalog.normalize_and_save(
        root_href="/Users/naman.jain/Desktop/personal/STACise/catalog",
        catalog_type=pystac.CatalogType.SELF_CONTAINED,
    )
