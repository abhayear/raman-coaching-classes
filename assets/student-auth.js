/** Shared student/staff auth helpers for paid courses. */
(function () {
  function client() {
    if (!window.DocumentCentre) return null;
    return DocumentCentre.supabaseClient();
  }

  async function getSession() {
    const c = client();
    if (!c) return null;
    const { data } = await c.auth.getSession();
    return data.session;
  }

  async function requireSignIn(email, password) {
    const c = client();
    const { data, error } = await c.auth.signInWithPassword({ email, password });
    if (error) throw error;
    return data.session;
  }

  async function signUp(email, password) {
    const c = client();
    const { data, error } = await c.auth.signUp({ email, password });
    if (error) throw error;
    return data;
  }

  async function signOut() {
    const c = client();
    if (c) await c.auth.signOut();
  }

  async function myPurchases() {
    const c = client();
    const session = await getSession();
    if (!c || !session) return [];
    const { data, error } = await c
      .from("purchases")
      .select("*, courses(*)")
      .eq("user_id", session.user.id)
      .eq("status", "completed");
    if (error) throw error;
    return data || [];
  }

  async function hasPurchased(courseId) {
    const c = client();
    const session = await getSession();
    if (!c || !session) return false;
    const { data, error } = await c
      .from("purchases")
      .select("id")
      .eq("user_id", session.user.id)
      .eq("course_id", courseId)
      .eq("status", "completed")
      .maybeSingle();
    if (error) return false;
    return !!data;
  }

  window.StudentAuth = {
    client,
    getSession,
    requireSignIn,
    signUp,
    signOut,
    myPurchases,
    hasPurchased,
  };
})();