from rumblet.classes.PetType import PetType


class PetTypeChart:
    types = {
        "Fire": PetType(name="Fire", strengths=["Grass"], weaknesses=["Water"], immunities=[]),
        "Water": PetType(name="Water", strengths=["Fire"], weaknesses=["Grass"], immunities=[]),
        "Grass": PetType(name="Grass", strengths=["Water"], weaknesses=["Fire"], immunities=[])
    }
    fire = types.get("Fire")
    water = types.get("Water")
    grass = types.get("Grass")

    @classmethod
    def get_multiplier(cls, attacking_type, defending_type):
        if attacking_type.name in defending_type.immunities:
            return 0
        elif defending_type.name in attacking_type.strengths:
            return 2
        elif defending_type.name in attacking_type.weaknesses:
            return 0.5
        else:
            return 1

    @classmethod
    def display_chart(cls):
        spacer = ' | '
        column_width = len(max(cls.types.keys(), key=len))
        row_headers = list(cls.types.keys())
        column_headers = ['*'.center(column_width)] + [row_header.center(column_width) for row_header in row_headers]
        header_row = spacer.join(column_headers)

        rows = list()
        rows.append(header_row)

        for row_header in row_headers:
            row = list()
            rows.append('-' * len(header_row))
            row.append(row_header.rjust(column_width))

            for column_header in column_headers[1:]:
                attacking_type = cls.types[row_header]
                defending_type = cls.types[column_header.strip()]

                if attacking_type.name in defending_type.immunities:  # Check for immunity first
                    value = '0'
                elif defending_type.name in attacking_type.strengths:
                    value = '2'
                elif defending_type.name in attacking_type.weaknesses:
                    value = '0.5'
                elif row_header == column_header.strip().replace('*', ''):
                    value = '1'
                else:
                    value = '-'

                row.append(value.center(column_width))

            rows.append(spacer.join(row))

        print('\n'.join(rows))


if __name__ == '__main__':
    PetTypeChart.display_chart()
