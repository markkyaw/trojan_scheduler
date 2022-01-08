import factory
from .models import BasicClassInfo, ClassSemester
import uuid

class BasicClassInfoFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = BasicClassInfo
	
	class_code = factory.Sequence(lambda n: "TCSS{}".format(uuid.uuid4().hex, n))
	class_section = factory.Sequence(lambda n: "CS Gang{}".format(n))
	year = 2022
	semester = ClassSemester.SPRING
	min_units = 4
	max_units = 4
	description = "Labore voluptas rerum inventore praesentium in doloremque officia non. Fugiat ipsam asperiores sed ipsa doloremque. Laborum nobis quod veritatis exercitationem eum reiciendis dolor. Et sit cum commodi assumenda assumenda officia dolore. Molestiae earum sint ratione soluta doloremque incidunt sint. Maxime ratione dolor rerum aliquam in. Laborum laudantium doloremque eos repellat iure omnis nihil. Distinctio repudiandae sit rem quia. Ut qui suscipit et laudantium. Deserunt hic cum provident eum nemo molestias at. In reiciendis et aut."