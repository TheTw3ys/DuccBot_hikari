import json

import hikari


class Leveling:
    @classmethod
    def get_leaderboard(cls, users_json) -> list:
        dictionary = {}
        with open(users_json, "r") as f:
            data = json.load(f)
            i = 0
            for member in data:
                exp = data[member].get("experience")
                i += 1
                if exp == 0:
                    continue
                new_dict = {
                    data[member].get("id"): exp
                }
                dictionary.update(new_dict)

                sorted_dict = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)

        return sorted_dict


class Administration:
    @classmethod
    def get_role(cls, server: hikari.Guild, name) -> hikari.Role.id:
        try:
            guild = server
            for role in guild.get_roles():
                if guild.get_role(role).name.lower() == name:
                    muted_role = guild.get_role(role)
                    return muted_role
        except hikari.NotFoundError:
            roles = server.get_roles()
            return roles

    @classmethod
    async def get_roles(cls, server: hikari.Guild):
        return server.get_roles()
