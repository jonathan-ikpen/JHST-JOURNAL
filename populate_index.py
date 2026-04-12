def populate_index():
    from journal.models import Page, PageSection
    page, _ = Page.objects.get_or_create(slug='index', defaults={'name': 'Home'})
    
    # Clear existing sections for home page to avoid duplicates
    PageSection.objects.filter(page=page).delete()
    
    sections = [
        {
            'key': 'introduction',
            'content': """
<section class="journal-intro">
  <div class="video-wrapper" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; background: #000; border-radius: 8px;">
    <iframe src="https://player.vimeo.com/video/1129153382" 
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
            frameborder="0" 
            allow="autoplay; fullscreen; picture-in-picture" 
            allowfullscreen>
    </iframe>
  </div>
</section>
            """.strip(),
            'order': 0
        },
        {
            'key': 'about_mission',
            'content': """
<section class="about-journal">
  <div class="mission-statement">
    <h3 class="text-xl font-bold mb-4 text-primary">MISSION STATEMENT</h3>
    <p class="mb-4 text-gray-700 leading-relaxed">Journal of Hydrocarbon Science and Technology (JHST) is the official publication of the Petroleum Training Institute, PTI, Effurun, Nigeria. The journal seeks to:</p>
    <ol class="list-decimal pl-6 space-y-3 text-gray-700">
      <li>Provide a global platform for original, peer-reviewed research that deepens understanding and drives innovation across the hydrocarbon value chain — from exploration and production to refining, environmental management, renewable integration, and digital transformation</li>
      <li>Provide the general public with dynamic and required information to the world for the purpose of innovation, knowledge/education, lifestyle, culture and career development.</li>
    </ol>
  </div>
</section>
            """.strip(),
            'order': 1
        },
        {
            'key': 'editors_desk',
            'content': """
<section class="editors-desk">
  <div class="editor-content flex flex-col md:flex-row gap-8 items-start">
    <div class="editor-photo flex-shrink-0 w-full md:w-64">
      <img src="/static/assets/images/chief_editor.jpg" alt="Engr. Henry I. Adimula" class="w-full rounded shadow-lg border-2 border-white">
    </div>
    <div class="editor-message flex-grow">
      <p class="mb-4 text-gray-700 leading-relaxed text-justify">In an era where the global energy landscape is undergoing unprecedented transformation, the Journal of Hydrocarbon Science and Technology (JHST) emerges as a timely response to a critical need — the need to rethink, redefine, and renew our approach to energy development, sustainability, and innovation.</p>
      <p class="mb-4 text-gray-700 leading-relaxed text-justify">The Petroleum Training Institute (PTI), for over five decades, has served as Nigeria’s premier institution for technical excellence in the petroleum and allied sectors. Through education, applied research, and industry collaboration, PTI has equipped generations of professionals with the competence and creativity to advance the oil and gas industry.</p>
      <p class="mb-6 text-gray-700 leading-relaxed text-justify">The JHST is a natural evolution of this legacy — a bridge between research and real-world application, between academia and industry, between innovation and impact.</p>
      <div class="mt-8 pt-6 border-t border-gray-100">
        <p class="font-bold text-xl text-primary mb-1">Engr. Henry I. Adimula</p>
        <p class="text-gray-600 font-medium italic">Principal/Chief Executive</p>
        <p class="text-gray-500 italic">Petroleum Training Institute</p>
      </div>
    </div>
  </div>
</section>
            """.strip(),
            'order': 2
        }
    ]
    
    for sec in sections:
        PageSection.objects.create(
            page=page,
            section_key=sec['key'],
            content_type='html',
            text_content=sec['content'],
            order=sec['order']
        )
    print(f"Successfully populated {len(sections)} sections for the index page.")

if __name__ == "__main__":
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal_system.settings')
    django.setup()
    populate_index()
