from src.core.cast_member.application.use_case.list_cast_member import (
    CastMemberOutput,
    ListCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repositry import (
    InMemoryCastMemberRepository,
)


class TestListCastMember:
    def test_list_cast_member(self):

        cast_member_repository = InMemoryCastMemberRepository()

        actor = CastMember(name="Peter", type=CastMemberType.ACTOR)
        director = CastMember(name="Christopher", type=CastMemberType.DIRECTOR)
        cast_member_repository.save(actor)
        cast_member_repository.save(director)

        use_case = ListCastMember(cast_member_repository)

        output = use_case.execute(input=ListCastMember.Input())

        assert len(output.data) == 2
        assert output == ListCastMember.Output(
            data=[
                CastMemberOutput(id=actor.id, name=actor.name, type=actor.type),
                CastMemberOutput(
                    id=director.id, name=director.name, type=director.type
                ),
            ]
        )

    def test_list_cast_member_with_empty_repository(self):
        cast_member_repository = InMemoryCastMemberRepository()
        use_case = ListCastMember(cast_member_repository)

        output = use_case.execute(input=ListCastMember.Input())

        assert len(output.data) == 0
