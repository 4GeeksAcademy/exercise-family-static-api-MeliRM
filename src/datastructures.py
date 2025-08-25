

from typing import List, Dict, Optional


class FamilyStructure:
    def __init__(self, last_name: str):
        self.last_name = last_name
        self._next_id = 1
        self._members: List[Dict] = []

    
    def _generate_id(self) -> int:
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member: Dict) -> Dict:
        """
        Agrega un miembro a la familia.
        - Genera 'id' si no viene.
        - Fuerza last_name al de la familia.
        Devuelve el miembro creado.
        """
        if "id" not in member or member["id"] is None:
            member["id"] = self._generate_id()
        else:
            
            if not isinstance(member["id"], int):
                raise ValueError("id must be an integer")
            if member["id"] >= self._next_id:
                self._next_id = member["id"] + 1

        
        member["last_name"] = self.last_name

    
        if not isinstance(member.get("first_name"), str) or not member["first_name"]:
            raise ValueError("first_name is required and must be a string")
        if not isinstance(member.get("age"), int) or member["age"] <= 0:
            raise ValueError("age is required and must be an integer > 0")
        if not isinstance(member.get("lucky_numbers"), list) or any(
            not isinstance(n, int) for n in member["lucky_numbers"]
        ):
            raise ValueError("lucky_numbers must be a list of integers")

        self._members.append({
            "id": member["id"],
            "first_name": member["first_name"],
            "last_name": self.last_name,
            "age": member["age"],
            "lucky_numbers": list(member["lucky_numbers"]),
        })
        return self._members[-1]

    def delete_member(self, id: int) -> bool:
        """
        Elimina el miembro con el id dado.
        Devuelve True si lo elimina, False si no existe.
        """
        for idx, m in enumerate(self._members):
            if m.get("id") == id:
                self._members.pop(idx)
                return True
        return False

    def get_member(self, id: int) -> Optional[Dict]:
        """
        Devuelve el miembro con el id dado o None si no existe.
        """
        for m in self._members:
            if m.get("id") == id:
                return m
        return None

    def get_all_members(self) -> List[Dict]:
        """
        Devuelve la lista completa de miembros.
        """
        return self._members
