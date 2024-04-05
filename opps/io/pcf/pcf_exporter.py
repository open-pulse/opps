from pathlib import Path

import numpy as np

from opps.model import Bend, Elbow, Flange, Pipe, Point


class PCFExporter:
    def __init__(self) -> None:
        pass

    def save(self, path, pipeline):
        path = Path(path).with_suffix(".pcf")
        var = self.encoder(pipeline)

        with open(path, "w", encoding="iso_8859_1") as file:
            file.write(var)

    def encoder(self, pipeline):
        string = self.encoder_header(pipeline)

        for structure in pipeline.structures:
            if isinstance(structure, Pipe):
                stringer = self.encoder_pipe(structure)
                string = string + "\n" + stringer

            elif isinstance(structure, Elbow):
                if structure.is_colapsed():
                    continue
                stringer = self.encoder_elbow(structure)
                string = string + "\n" + stringer

            elif isinstance(structure, Bend):
                if structure.is_colapsed():
                    continue
                stringer = self.encoder_bend(structure)
                string = string + "\n" + stringer

            elif isinstance(structure, Flange):
                stringer = self.encoder_flange(structure)
                string = string + "\n" + stringer

        return string

    def encoder_header(self, pipeline):
        string = (
            "ISOGEN-FILES            ISOGEN.FLS                  \n"
            "UNITS-BORE              MM                          \n"
            "UNITS-CO-ORDS           MM                          \n"
            "UNITS-BOLT-LENGTH       MM                          \n"
            "UNITS-BOLT-DIA          MM                          \n"
            "UNITS-WEIGHT            KGS                         \n"
            "PIPELINE-REFERENCE      CFG1                        \n"
            "PIPING-SPEC         CS150                           \n"
            "START-CO-ORDS       0.0000       0.0000      0.0000 \n"
        )

        return string

    def encoder_pipe(self, pipe):
        start_x = round(pipe.start.x * 1_000, 5)
        start_y = round(pipe.start.y * 1_000, 5)
        start_z = round(pipe.start.z * 1_000, 5)
        start_diameter = round(pipe.start_diameter * 1_000, 5)

        end_x = round(pipe.end.x * 1_000, 5)
        end_y = round(pipe.end.y * 1_000, 5)
        end_z = round(pipe.end.z * 1_000, 5)
        end_diameter = round(pipe.end_diameter * 1_000, 5)

        # The format specifier >14 reserves 14 spaces to show the data
        # and align it to the right
        string = (
            "PIPE \n"
            f"    END-POINT {start_x:abacaxi}, {start_y:>14} {start_z:>14} {start_diameter:>14} \n"
            f"    END-POINT {end_x:>14}, {end_y:>14} {end_z:>14} {end_diameter:>14} \n"
        )
        return string

    def encoder_bend(self, bend):
        string = f"""BEND
    END-POINT{round(1000*bend.start.x):>17.4f}{round(1000*bend.start.y):>13.4f}{round(1000*bend.start.z):>13.4f}{round(1000*bend.start_diameter):>15.4f}  
    END-POINT{round(1000*bend.end.x):>17.4f}{round(1000*bend.end.y):>13.4f}{round(1000*bend.end.z):>13.4f}{round(1000*bend.end_diameter):>15.4f}   
    CENTRE-POINT{round(1000*bend.corner.x):>14.4f}{round(1000*bend.corner.y):>13.4f}{round(1000*bend.corner.z):>13.4f}   
    SKEY BEBW"""

        return string

    def encoder_flange(self, flange):
        end_x = round(flange.position.x + flange.normal[0], 2)
        end_y = round(flange.position.y + flange.normal[1], 2)
        end_z = round(flange.position.z + flange.normal[2], 2)

        string = f"""FLANGE
    END-POINT{round(1000*flange.position.x):>14.4f}{round(1000*flange.position.y):>13.4f}{round(1000*flange.position.z):>13.4f}{round(1000*flange.diameter):>15.4f}   
    END-POINT{1000*end_x:>14.4f}{1000*end_y:>13.4f}{1000*end_z:>13.4f}{round(1000*flange.diameter):>15.4f}   
    SKEY FLBL"""

        return string

    def encoder_elbow(self, bend):
        string = f"""ELBOW
    END-POINT{round(1000*bend.start.x):>14.4f}{round(1000*bend.start.y):>11.4f}{round(1000*bend.start.z):>13.4f}{round(1000*bend.start_diameter):>13.4f}   
    END-POINT{round(1000*bend.end.x):>14.4f}{round(1000*bend.end.y):>11.4f}{round(1000*bend.end.z):>13.4f}{round(1000*bend.end_diameter):>13.4f}   
    CENTRE-POINT{round(1000*bend.corner.x):>14.4f}{round(1000*bend.corner.y):>11.4f}{round(1000*bend.corner.z):>13.4f}        
    SKEY                 ELBW"""

        return string
