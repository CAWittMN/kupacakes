from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from openai import OpenAI
import json

# Create your models here.


class KeyIngredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Cupcake(models.Model):
    valid = models.BooleanField(default=False)
    stupid_article = models.TextField(null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    recipe = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cupcakes", null=True
    )
    key_ingredients = models.ManyToManyField(KeyIngredient)

    def __str__(self):
        return f"{self.name} - {self.user.username} - {self.created_at}"

    @classmethod
    def generate_cupcake(cls, user_input):
        ai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        assistant_id = settings.OPENAI_ASSISTANT_ID
        message_thread = ai_client.beta.threads.create(
            messages=[{"role": "user", "content": json.dumps(user_input)}]
        )
        thread_id = message_thread.id
        run = ai_client.beta.threads.runs.create_and_poll(
            assistant_id=assistant_id, thread_id=thread_id
        )
        if run.status == "completed":
            messages = ai_client.beta.threads.messages.list(thread_id, run_id=run.id)
            data = json.loads(messages.data[0].content[0].text.value)
            if hasattr(data, "valid") and not data["valid"]:
                return data
            img_prompt = data["prompt"]
            img_response = ai_client.images.generate(
                model="dall-e-3",
                prompt=img_prompt,
                n=1,
                size="1024x1024",
                response_format="url",
            )
            data["image_url"] = img_response.data[0].url
            data.pop("prompt")
            new_cupcake = cls(**data)

        return new_cupcake
