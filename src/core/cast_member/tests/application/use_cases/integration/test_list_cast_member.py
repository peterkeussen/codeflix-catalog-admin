from src.core.cast_member.application.use_case.list_cast_member import (
    CastMemberOutput,
    ListCastMember,
    ListCastMemberOutputMeta,
    ListCastMemberRequest,
    ListCastMemberResponse,
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
        input = ListCastMemberRequest()
        output = use_case.execute(input)

        assert len(output.data) == 2
        assert output == ListCastMemberResponse(
            data=[
                CastMemberOutput(
                    id=director.id, name=director.name, type=director.type
                ),
                CastMemberOutput(id=actor.id, name=actor.name, type=actor.type),
            ],
            meta=ListCastMemberOutputMeta(
                current_page=1,
                page_size=10,
                total=2,
            ),
        )

    def test_list_cast_member_with_empty_repository(self):
        cast_member_repository = InMemoryCastMemberRepository()
        use_case = ListCastMember(cast_member_repository)
        input = ListCastMemberRequest()
        output = use_case.execute(input)

        assert len(output.data) == 0
